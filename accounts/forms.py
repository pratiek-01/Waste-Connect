from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class DonorSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'organization_name', 'phone', 'city', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.DONOR
        if commit:
            user.save()
        return user


class NGOSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'organization_name', 'phone', 'city',
                  'address', 'registration_doc']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.NGO
        user.is_verified = False  # admin must verify before NGO can claim listings
        if commit:
            user.save()
        return user
