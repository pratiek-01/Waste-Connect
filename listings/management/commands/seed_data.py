from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from accounts.models import User
from listings.models import Listing


class Command(BaseCommand):
    help = "Adds simple sample data: 2 donors, 2 NGOs, 4 listings"

    def handle(self, *args, **options):

        # ---------- STEP 1: Create Donor users ----------
        donor1 = User.objects.create_user(
            username="tajhotel",
            password="password123",
            role="donor",
            organization_name="Taj Hotel",
            city="Bhopal",
            address="Shamla Hills, Bhopal",
        )

        donor2 = User.objects.create_user(
            username="spicegarden",
            password="password123",
            role="donor",
            organization_name="Spice Garden Restaurant",
            city="Bhopal",
            address="MP Nagar, Bhopal",
        )

        # ---------- STEP 2: Create NGO users ----------
        ngo1 = User.objects.create_user(
            username="annapurna_ngo",
            password="password123",
            role="ngo",
            organization_name="Annapurna Food Bank",
            city="Bhopal",
            address="New Market, Bhopal",
            is_verified=True,   # already verified, so it can claim listings
        )

        ngo2 = User.objects.create_user(
            username="umeed_trust",
            password="password123",
            role="ngo",
            organization_name="Umeed Trust",
            city="Indore",
            address="Rajwada, Indore",
            is_verified=False,  # not verified yet
        )

        # ---------- STEP 3: Create some Listings (food donations) ----------
        now = timezone.now()

        Listing.objects.create(
            donor=donor1,
            title="50 Plates Veg Thali",
            description="Leftover veg thali from a wedding function.",
            category="cooked_food",
            quantity="50 plates",
            city="Bhopal",
            pickup_address="Shamla Hills, Bhopal",
            expiry_time=now + timedelta(hours=5),
            status="pending",
        )

        Listing.objects.create(
            donor=donor2,
            title="20kg Rice and Dal",
            description="Extra raw rice and dal stock, sealed packets.",
            category="raw_ingredients",
            quantity="20 kg",
            city="Bhopal",
            pickup_address="MP Nagar, Bhopal",
            expiry_time=now + timedelta(hours=48),
            status="pending",
        )

        Listing.objects.create(
            donor=donor1,
            title="30 Plates Paneer Curry and Roti",
            description="Banquet leftovers, good for immediate pickup.",
            category="cooked_food",
            quantity="30 plates",
            city="Bhopal",
            pickup_address="Shamla Hills, Bhopal",
            expiry_time=now + timedelta(hours=3),
            status="claimed",
            claimed_by=ngo1,
        )

        Listing.objects.create(
            donor=donor2,
            title="Old Blankets and Clothes",
            description="Gently used blankets and winter clothes.",
            category="clothes",
            quantity="40 pieces",
            city="Bhopal",
            pickup_address="MP Nagar, Bhopal",
            expiry_time=now + timedelta(hours=240),
            status="delivered",
            claimed_by=ngo1,
        )

        # ---------- DONE ----------
        self.stdout.write(self.style.SUCCESS("Sample data added successfully!"))
        self.stdout.write("Login with: tajhotel / spicegarden / annapurna_ngo / umeed_trust")
        self.stdout.write("Password for all: password123")
