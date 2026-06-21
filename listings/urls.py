from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),

    # Donor
    path('donor/dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('listing/create/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/status/', views.update_listing_status, name='update_status'),

    # NGO / public browse
    path('browse/', views.browse_listings, name='browse_listings'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:pk>/claim/', views.claim_listing, name='claim_listing'),
    path('ngo/dashboard/', views.ngo_dashboard, name='ngo_dashboard'),
]
