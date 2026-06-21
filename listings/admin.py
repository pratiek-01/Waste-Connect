from django.contrib import admin
from django.db.models import Count
from .models import Listing, LogisticsUpdate


class LogisticsInline(admin.TabularInline):
    model = LogisticsUpdate
    extra = 0
    readonly_fields = ('status', 'note', 'updated_by', 'timestamp')


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'donor', 'claimed_by', 'city', 'category',
                     'status', 'is_flagged', 'expiry_time', 'created_at')
    list_filter = ('status', 'category', 'city', 'is_flagged')
    search_fields = ('title', 'donor__username', 'claimed_by__username')
    inlines = [LogisticsInline]
    actions = ['flag_listings', 'unflag_listings', 'delete_stale_listings']

    @admin.action(description="Flag selected listings as suspicious")
    def flag_listings(self, request, queryset):
        queryset.update(is_flagged=True)

    @admin.action(description="Remove flag")
    def unflag_listings(self, request, queryset):
        queryset.update(is_flagged=False)

    @admin.action(description="Delete expired/stale listings")
    def delete_stale_listings(self, request, queryset):
        count = queryset.filter(status='pending').count()
        queryset.filter(status='pending').delete()
        self.message_user(request, f"Deleted {count} stale listing(s).")

    def changelist_view(self, request, extra_context=None):
        # Simple analytics injected into the admin changelist page
        extra_context = extra_context or {}
        extra_context['status_counts'] = (
            Listing.objects.values('status').annotate(total=Count('id'))
        )
        extra_context['category_counts'] = (
            Listing.objects.values('category').annotate(total=Count('id'))
        )
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(LogisticsUpdate)
class LogisticsUpdateAdmin(admin.ModelAdmin):
    list_display = ('listing', 'status', 'updated_by', 'timestamp')
    list_filter = ('status',)
