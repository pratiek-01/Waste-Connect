from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import DonorSignupForm, NGOSignupForm


def signup_choice(request):
    """Landing page asking: sign up as Donor or as NGO?"""
    return render(request, 'accounts/signup_choice.html')


def donor_signup(request):
    if request.method == 'POST':
        form = DonorSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to WasteConnect! You can now list donations.")
            return redirect('listings:donor_dashboard')
    else:
        form = DonorSignupForm()
    return render(request, 'accounts/signup.html', {'form': form, 'role': 'Donor'})


def ngo_signup(request):
    if request.method == 'POST':
        form = NGOSignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Registered! Your account needs admin verification "
                                    "before you can claim donations. We'll notify you.")
            return redirect('accounts:login')
    else:
        form = NGOSignupForm()
    return render(request, 'accounts/signup.html', {'form': form, 'role': 'NGO'})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user_obj': request.user})
