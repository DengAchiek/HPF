import datetime
from django.db import migrations, models


NEWS_ITEMS = [
    {
        "title": "RANA Bootcamp advances epidemic preparedness across Africa",
        "date_label": "28-30 April 2026",
        "event_date": datetime.date(2026, 4, 28),
        "venue": "The Tribe Hotel, Nairobi, Kenya",
        "participants": "Civil society and community organizations from 11 African countries",
        "summary": "The Resilience Action Network Africa (RANA), in partnership with Resolve to Save Lives, convened civil society and community organizations from 11 African countries to establish a shared agenda for epidemic preparedness and community-engaged disease surveillance. HFPZ was represented by Executive Director Doreen McGeachy.",
        "static_image": "images/news/rana-bootcamp-2026.jpg",
        "image_alt": "Plenary session at the RANA Bootcamp in Nairobi",
        "sort_order": 5,
    },
    {
        "title": "HFPZ joins continental dialogue on demographic dividend and reproductive health",
        "date_label": "8-10 April 2026",
        "event_date": datetime.date(2026, 4, 8),
        "venue": "Intercontinental Hotel, Lusaka, Zambia",
        "participants": "Over 200 delegates from across Africa",
        "summary": "The 1st Continental Conference for Non-State Actors on the Demographic Dividend and Reproductive Health brought together civil society, academia, private sector leaders, and youth advocates. HFPZ Programs Manager Nolia Chipundo participated in the dialogue supporting the Lusaka 2026 Call for Action.",
        "static_image": "images/news/continental-conference-lusaka-2026.jpg",
        "image_alt": "Delegates at the continental conference plenary session in Lusaka",
        "sort_order": 6,
    },
]


def seed_document_news(apps, schema_editor):
    NewsItem = apps.get_model("core", "NewsItem")
    for item in NEWS_ITEMS:
        title = item["title"]
        defaults = item.copy()
        defaults["is_active"] = True
        NewsItem.objects.update_or_create(title=title, defaults=defaults)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_partnerlogo"),
    ]

    operations = [
        migrations.AddField(
            model_name="newsitem",
            name="event_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="newsitem",
            name="participants",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="newsitem",
            name="venue",
            field=models.CharField(blank=True, max_length=180),
        ),
        migrations.RunPython(seed_document_news, migrations.RunPython.noop),
    ]
