from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from .models import Listing, LogisticsUpdate
from .forms import ListingForm, ListingFilterForm


def home(request):
    """Public landing page — shows a few latest active listings."""
    recent = Listing.objects.filter(status='pending').order_by('-created_at')[:6]
    return render(request, 'listings/home.html', {'recent': recent})


def dashboard_redirect(request):
    """After login, send user to the right dashboard based on role."""
    if request.user.role == 'donor':
        return redirect('listings:donor_dashboard')
    elif request.user.role == 'ngo':
        return redirect('listings:browse_listings')
    return redirect('listings:home')


# ---------------------------------------------------------------------------
# DONOR SIDE
# ---------------------------------------------------------------------------

@login_required
def donor_dashboard(request):
    if request.user.role != 'donor':
        messages.error(request, "Only donors can access this page.")
        return redirect('listings:home')

    listings = request.user.listings.all().order_by('-created_at')

    paginator = Paginator(listings, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listings/donor_dashboard.html', {'page_obj': page_obj})


@login_required
def create_listing(request):
    if request.user.role != 'donor':
        messages.error(request, "Only donors can create listings.")
        return redirect('listings:home')

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.donor = request.user
            listing.city = listing.city or request.user.city
            listing.save()
            messages.success(request, "Listing posted! NGOs nearby can now see it.")
            return redirect('listings:donor_dashboard')
    else:
        form = ListingForm(initial={'city': request.user.city})

    return render(request, 'listings/listing_form.html', {'form': form})


@login_required
def update_listing_status(request, pk):
    """Donor or claiming NGO moves the listing through its logistics lifecycle."""
    listing = get_object_or_404(Listing, pk=pk)

    is_owner = listing.donor_id == request.user.id
    is_claimer = listing.claimed_by_id == request.user.id
    if not (is_owner or is_claimer):
        messages.error(request, "You don't have permission to update this listing.")
        return redirect('listings:home')

    new_status = request.POST.get('status')
    valid_transitions = dict(Listing.STATUS_CHOICES)
    if new_status in valid_transitions:
        listing.status = new_status
        if new_status == 'delivered':
            listing.delivered_at = timezone.now()
        listing.save()
        LogisticsUpdate.objects.create(
            listing=listing, status=new_status, updated_by=request.user
        )
        messages.success(request, f"Status updated to '{valid_transitions[new_status]}'.")

    return redirect('listings:listing_detail', pk=pk)


# ---------------------------------------------------------------------------
# NGO SIDE — search, filter, pagination, claim
# ---------------------------------------------------------------------------

def browse_listings(request):
    """Public/NGO browse page with location + category search/filter + pagination."""
    listings = Listing.objects.filter(status='pending', expiry_time__gte=timezone.now())

    filter_form = ListingFilterForm(request.GET or None)
    if filter_form.is_valid():
        city = filter_form.cleaned_data.get('city')
        category = filter_form.cleaned_data.get('category')
        q = filter_form.cleaned_data.get('q')

        if city:
            listings = listings.filter(city__icontains=city)
        if category:
            listings = listings.filter(category=category)
        if q:
            listings = listings.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )

    listings = listings.order_by('expiry_time')

    paginator = Paginator(listings, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listings/browse.html', {
        'page_obj': page_obj,
        'filter_form': filter_form,
    })


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'listings/listing_detail.html', {'listing': listing})


@login_required
def claim_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, status='pending')

    if request.user.role != 'ngo':
        messages.error(request, "Only NGOs can claim donations.")
        return redirect('listings:listing_detail', pk=pk)

    if not request.user.is_verified:
        messages.error(request, "Your NGO account is pending admin verification.")
        return redirect('listings:listing_detail', pk=pk)

    listing.claimed_by = request.user
    listing.status = 'claimed'
    listing.claimed_at = timezone.now()
    listing.save()

    LogisticsUpdate.objects.create(
        listing=listing, status='claimed', updated_by=request.user,
        note=f"Claimed by {request.user.organization_name or request.user.username}"
    )

    messages.success(request, "Donation claimed! Coordinate pickup with the donor.")
    return redirect('listings:listing_detail', pk=pk)


@login_required
def ngo_dashboard(request):
    if request.user.role != 'ngo':
        return redirect('listings:home')

    claims = request.user.claimed_listings.all().order_by('-claimed_at')
    paginator = Paginator(claims, 8)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'listings/ngo_dashboard.html', {'page_obj': page_obj})
