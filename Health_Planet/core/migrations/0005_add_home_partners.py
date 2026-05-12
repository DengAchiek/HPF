from django.db import migrations


PARTNERS = [
    (
        "images/partners/ministry-health.svg",
        "Ministry of Health logo",
        "Ministry of Health",
        "partner-wide",
        10,
    ),
    (
        "images/partners/rana.svg",
        "RANA logo",
        "RANA",
        "partner-wide",
        20,
    ),
    (
        "images/partners/resolve-to-save-lives.svg",
        "Resolve to Save Lives logo",
        "Resolve to Save Lives",
        "partner-wide",
        30,
    ),
    (
        "images/partners/thrive-aid.svg",
        "Thrive Aid logo",
        "Thrive Aid",
        "partner-square",
        40,
    ),
    (
        "images/partners/ministry-community-development-social-services.svg",
        "Ministry of Community Development and Social Services logo",
        "Ministry of Community Development and Social Services",
        "partner-wide",
        50,
    ),
    (
        "images/partners/ministry-green-economy-environment.svg",
        "Ministry of Green Economy and Environment logo",
        "Ministry of Green Economy and Environment",
        "partner-wide",
        60,
    ),
]


def add_home_partners(apps, schema_editor):
    SectionContent = apps.get_model("core", "SectionContent")
    GalleryImage = apps.get_model("core", "GalleryImage")

    SectionContent.objects.update_or_create(
        page_slug="home",
        key="home_partners",
        defaults={
            "kicker": "Partners",
            "title": "Our partners",
            "body": "Health Planet Foundation works alongside public institutions and implementing partners to strengthen community health, resilience, and public service delivery.",
            "static_image": "",
            "image_alt": "",
            "image_caption": "",
            "button_label": "",
            "button_url_name": "",
            "button_external_url": "",
        },
    )

    for static_image, image_alt, caption, focus_class, sort_order in PARTNERS:
        GalleryImage.objects.update_or_create(
            gallery_key="home_partners",
            static_image=static_image,
            defaults={
                "image_alt": image_alt,
                "caption": caption,
                "focus_class": focus_class,
                "sort_order": sort_order,
                "is_active": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_update_home_what_we_do"),
    ]

    operations = [
        migrations.RunPython(add_home_partners, migrations.RunPython.noop),
    ]
