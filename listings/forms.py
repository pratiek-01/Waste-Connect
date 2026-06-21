from django import forms
from .models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'quantity',
                  'city', 'pickup_address', 'expiry_time', 'image']
        widgets = {
            'expiry_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ListingFilterForm(forms.Form):
    city = forms.CharField(required=False)
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Categories')] + Listing.CATEGORY_CHOICES
    )
    q = forms.CharField(required=False, label="Search")
