# Health Planet Foundation Website

Health Planet Foundation is a Django-powered public website and content management system for Health Planet Foundation Zambia. The site presents the foundation's programs, projects, news, partners, contact information, donation interest workflow, and application workflows for careers and internships.

The frontend is built with Django templates and custom CSS. Most public content can be updated from the Django admin site.

## Features

- Admin-managed page content, hero sections, navigation, footer links, focus areas, partners, projects, news, and site settings.
- Project impact pages with long-form stories, outcome lists, images, locations, and project periods.
- Newspaper-style news pages with article detail pages and optional venue, date, participant, and gallery fields.
- Career and internship application forms with admin inbox records, privacy consent, optional CV or portfolio URL, and spam honeypot protection.
- Contact and donation enquiry workflows stored in the admin site, with optional email notifications.
- SEO support with page meta descriptions, canonical URLs, Open Graph/Twitter tags, `sitemap.xml`, and `robots.txt`.
- Optional Google Analytics 4 tracking controlled through admin site settings and visitor consent.
- Health check endpoint at `/health/` for uptime monitoring.
- Render deployment support with PostgreSQL and WhiteNoise static file serving.

## Project Structure

```text
.
├── Health_Planet/
│   ├── Health_Planet/        # Django project settings, URLs, WSGI
│   ├── core/                 # Main CMS models, views, admin, migrations
│   ├── careers/              # Career openings and application submissions
│   ├── contacts/             # Contact submissions
│   ├── donations/            # Donation interest submissions
│   ├── internships/          # Internship tracks
│   ├── news/                 # App shell for news routes
│   ├── projects/             # App shell for projects routes
│   ├── static/               # CSS, images, and static assets
│   ├── templates/            # Public Django templates
│   ├── manage.py
│   └── requirements.txt
├── render.yaml               # Render web service and PostgreSQL blueprint
├── requirements.txt          # Root requirements file used by Render
└── README.md
```

## Requirements

- Python 3.12 or newer
- pip
- SQLite for local development, or PostgreSQL when `DATABASE_URL` is set

The production deployment uses PostgreSQL through `DATABASE_URL`.

## Local Setup

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python Health_Planet/manage.py migrate
python Health_Planet/manage.py createsuperuser
python Health_Planet/manage.py runserver
```

Open the site at:

```text
http://127.0.0.1:8000/
```

Open the admin site at:

```text
http://127.0.0.1:8000/admin/
```

Local development uses `Health_Planet/db.sqlite3` when `DATABASE_URL` is not set.

## Useful Commands

Run system checks:

```bash
python Health_Planet/manage.py check
```

Run tests:

```bash
python Health_Planet/manage.py test
```

Create migrations after model changes:

```bash
python Health_Planet/manage.py makemigrations
```

Apply migrations:

```bash
python Health_Planet/manage.py migrate
```

Collect static files:

```bash
python Health_Planet/manage.py collectstatic --noinput
```

## Environment Variables

Common environment variables:

```text
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=your-domain.com,.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://*.onrender.com
DATABASE_URL=postgresql://...
DATABASE_SSL_REQUIRE=True
```

Email notification variables are optional. Submissions are stored in the admin site even if email is not configured.

```text
DEFAULT_FROM_EMAIL=website@example.com
CONTACT_NOTIFICATION_EMAIL=team@example.com
DONATION_NOTIFICATION_EMAIL=team@example.com
APPLICATION_NOTIFICATION_EMAIL=team@example.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
EMAIL_USE_TLS=True
```

Analytics is configured in the Django admin through **Site settings** by adding a GA4 Measurement ID.

## Render Deployment

This repository includes `render.yaml` for a Render web service and PostgreSQL database.

Build command:

```bash
pip install -r requirements.txt && python Health_Planet/manage.py collectstatic --noinput
```

Start command:

```bash
python Health_Planet/manage.py migrate --noinput && gunicorn --chdir Health_Planet Health_Planet.wsgi:application
```

For an existing manually configured Render service:

1. Create a Render PostgreSQL database in the same region as the web service.
2. Copy the database **Internal Database URL**.
3. Add it to the web service environment variables as `DATABASE_URL`.
4. Set the start command to the command shown above.
5. Deploy the latest commit.

After deployment, create an admin account from the Render shell:

```bash
python Health_Planet/manage.py createsuperuser
```

Do not run `makemigrations` on Render. Migration files should be committed locally and pushed to GitHub.

## Admin Content

The Django admin can update:

- Site settings, logo, contact details, analytics ID, and footer text
- Page hero content and SEO descriptions
- Navigation and footer links
- Home sections, stats, feature cards, community images, and partners
- Focus areas
- Projects and project impact galleries
- News articles and news galleries
- Career openings and internship tracks
- Contact, donation, and application submissions

Seeded default content is included in migrations so a fresh PostgreSQL database starts with working public pages.

## Static And Media Files

Static files are stored in `Health_Planet/static/` and served in production through WhiteNoise after `collectstatic`.

Admin-uploaded media files use Django's filesystem storage under `Health_Planet/media/`. On Render, filesystem uploads are not durable unless you attach persistent storage or move media uploads to an external storage service.

## Public Routes

```text
/
/about/
/projects/
/projects/<slug>/
/focus-areas/<slug>/
/news/
/news/<slug>/
/careers/
/careers/apply/
/internships/
/internships/apply/
/donate/
/contact/
/privacy/
/sitemap.xml
/robots.txt
/health/
/admin/
```

## Maintenance Notes

- Keep migrations committed before deployment.
- Use PostgreSQL in production through `DATABASE_URL`; Render deployment intentionally refuses to run without it.
- Use the internal database URL on Render, not the external database URL.
- Existing SQLite data does not automatically move to PostgreSQL. Export/import data if preserving old admin records is required.
