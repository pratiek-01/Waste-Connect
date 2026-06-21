from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with role-based access.
    ROLE decides which dashboard the user sees and what they can do.
    """
    DONOR = 'donor'
    NGO = 'ngo'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (DONOR, 'Donor (Restaurant/Hotel/Event)'),
        (NGO, 'NGO / Shelter (Receiver)'),
        (ADMIN, 'Platform Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=DONOR)
    phone = models.CharField(max_length=15, blank=True)
    organization_name = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)

    # Only relevant for NGOs — admin verifies before they can claim listings
    is_verified = models.BooleanField(default=False)
    registration_doc = models.FileField(
        upload_to='ngo_docs/', blank=True, null=True,
        help_text="Registration certificate / proof (required for NGOs)"
    )

    def is_donor(self):
        return self.role == self.DONOR

    def is_ngo(self):
        return self.role == self.NGO

    def __str__(self):
        return f"{self.username} ({self.role})"
