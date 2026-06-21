from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'organization_name', 'city', 'is_verified')
    list_filter = ('role', 'is_verified', 'city')
    search_fields = ('username', 'email', 'organization_name')

    fieldsets = UserAdmin.fieldsets + (
        ('WasteConnect Profile', {
            'fields': ('role', 'phone', 'organization_name', 'address', 'city',
                       'is_verified', 'registration_doc')
        }),
    )

    actions = ['verify_ngos']

    @admin.action(description="Verify selected NGOs")
    def verify_ngos(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} NGO(s) verified successfully.")
