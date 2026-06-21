# WasteConnect — Hyperlocal Food & Resource Redistribution Network

A Django backend project connecting Donors (restaurants/hotels/event venues)
with verified NGOs/shelters for surplus food & resource redistribution.

## Setup (local machine — needs internet to install Django)

```bash
# 1. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations (creates the database tables from models.py)
python manage.py makemigrations
python manage.py migrate

# 4. Create a superuser (this becomes your Admin Panel login)
python manage.py createsuperuser

# 5. Run the dev server
python manage.py runserver
```

Visit:
- `http://127.0.0.1:8000/` — public homepage
- `http://127.0.0.1:8000/accounts/signup/` — Donor / NGO signup
- `http://127.0.0.1:8000/browse/` — browse donations (search/filter/pagination)
- `http://127.0.0.1:8000/admin/` — Admin Panel (verify NGOs, flag/delete listings, see analytics)

## Project structure

```
wasteconnect/
├── manage.py
├── requirements.txt
├── wasteconnect/          # project settings, root urls
├── accounts/              # custom User model (role: donor/ngo/admin), signup/login
├── listings/               # Listing + LogisticsUpdate models, dashboards, search, claim flow
├── templates/              # plain HTML templates (no Bootstrap/Tailwind)
└── static/css/style.css    # hand-written minimal CSS
```

## How each requirement is implemented

| Requirement | Where |
|---|---|
| Role-based auth | `accounts/models.py` (`User.role`), separate signup forms & dashboards |
| ORM relationships | `listings/models.py` — Donor → many Listings (FK), Listing → one claiming NGO (FK), Listing → many LogisticsUpdate (audit trail) |
| Search & filter | `listings/views.py::browse_listings` — filters by city, category, keyword |
| Pagination | `Paginator` used in `browse_listings`, `donor_dashboard`, `ngo_dashboard` |
| Admin panel | `accounts/admin.py` (verify NGOs action), `listings/admin.py` (flag/delete stale listings, status & category analytics injected into changelist) |

## Next steps you might add
- Email notification when a listing is claimed
- Google Maps/PIN-based distance filtering instead of plain city text match
- REST API (Django REST Framework) if you want a separate frontend/mobile app later
- Celery task to auto-expire stale listings instead of manual admin action
