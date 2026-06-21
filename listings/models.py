from django.db import models
from django.conf import settings
from django.utils import timezone


class Listing(models.Model):
    """
    A donation listed by a Donor (restaurant/hotel/event).
    One Donor -> many Listings (FK).
    One Listing -> claimed by at most one NGO (FK, nullable until claimed).
    """

    CATEGORY_CHOICES = [
        ('cooked_food', 'Cooked Food'),
        ('raw_ingredients', 'Raw Ingredients / Groceries'),
        ('packaged_food', 'Packaged Food'),
        ('clothes', 'Clothes'),
        ('other', 'Other Resources'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending (Unclaimed)'),
        ('claimed', 'Claimed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('expired', 'Expired'),
    ]

    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings',
        limit_choices_to={'role': 'donor'},
    )
    claimed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='claimed_listings',
        limit_choices_to={'role': 'ngo'},
    )

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='cooked_food')
    quantity = models.CharField(max_length=50, help_text="e.g. '20 plates', '15 kg'")

    city = models.CharField(max_length=100)
    pickup_address = models.CharField(max_length=255)

    expiry_time = models.DateTimeField(help_text="When this donation is no longer usable")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')

    image = models.ImageField(upload_to='listings/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    claimed_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    # Admin moderation
    is_flagged = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    @property
    def is_expired(self):
        return self.expiry_time < timezone.now() and self.status not in ('delivered',)


class LogisticsUpdate(models.Model):
    """
    Tracks the journey of a claimed listing.
    One Listing -> many LogisticsUpdate entries (audit trail of status changes).
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='logistics_updates')
    status = models.CharField(max_length=15, choices=Listing.STATUS_CHOICES)
    note = models.CharField(max_length=255, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.listing.title} -> {self.status}"
