from django.db import migrations


HOME_FEATURES = [
    (
        "01",
        "CLIMATE RESILIENCE & AGRICULTURE",
        'Training communities in climate-smart agriculture and agroforestry to boost food security.\n\nTree Planting & Reforestation: Engaging in community-driven afforestation to restore landscapes, improve biodiversity, and prevent soil erosion.\n\nWaste Segregation & Management: Implementing "waste-to-wealth" projects in peri-urban areas to convert solid waste into compost and recyclable products.',
        10,
    ),
    (
        "02",
        "WASH",
        "(Water, Sanitation, and Hygiene): Improving access to safe water and sanitation to build resilience against extreme weather.",
        20,
    ),
    (
        "03",
        "MENTAL HEALTH MANAGEMENT",
        "Integrating mental health support for communities affected by climate disasters, droughts, and poverty.",
        30,
    ),
    (
        "04",
        "SAFE MOTHERHOOD",
        "Family Planning & Health: Promoting sustainable population growth and reproductive health services in communities.",
        40,
    ),
    (
        "05",
        "SRH AWARENESS",
        "Raising awareness on sexual and reproductive health rights, family planning, and gender-based violence prevention.",
        50,
    ),
    (
        "06",
        "EPIDEMIC PREPAREDNESS",
        "Strengthening community readiness and response to disease outbreaks through training and early warning systems.",
        60,
    ),
    (
        "07",
        "ADVOCACY & HEALTH PROMOTIONS",
        "Advocating for community health rights and promoting healthy behaviours through campaigns, media, and grassroots engagement.",
        70,
    ),
]


def update_home_features(apps, schema_editor):
    FeatureCard = apps.get_model("core", "FeatureCard")
    FeatureCard.objects.filter(section_key="home_features").update(is_active=False)

    for icon, title, body, sort_order in HOME_FEATURES:
        FeatureCard.objects.update_or_create(
            section_key="home_features",
            title=title,
            defaults={
                "icon": icon,
                "body": body,
                "sort_order": sort_order,
                "is_active": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_update_staff_directory"),
    ]

    operations = [
        migrations.RunPython(update_home_features, migrations.RunPython.noop),
    ]
