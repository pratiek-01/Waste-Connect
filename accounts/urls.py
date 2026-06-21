from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_choice, name='signup_choice'),
    path('signup/donor/', views.donor_signup, name='donor_signup'),
    path('signup/ngo/', views.ngo_signup, name='ngo_signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
]
