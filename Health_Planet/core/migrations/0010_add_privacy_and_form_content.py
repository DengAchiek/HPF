from django.db import migrations


DONATE_BODY = (
    "Tell us how you would like to support the work. Our team will contact you "
    "with approved giving options. No online payment is collected on this form."
)

PRIVACY_SECTIONS = [
    (
        "privacy_intro",
        "Last updated: 25 May 2026",
        "How we handle your information",
        "Health Planet Foundation collects only the details needed to respond to "
        "enquiries and expressions of interest in supporting our work.",
    ),
    (
        "privacy_information",
        "",
        "Information we collect",
        "When you use the contact form, we collect your name, email address, "
        "optional phone and organization details, and your message.\n\nWhen you "
        "submit donation interest, we collect your contact details, preferred "
        "contribution amount, and any note you provide. This form does not collect "
        "card, mobile money, or bank payment details.",
    ),
    (
        "privacy_use",
        "",
        "How we use it",
        "We use submissions to answer enquiries, discuss partnerships, and follow "
        "up about voluntary support. Authorized staff may review submissions in "
        "the website administration system and may receive an email alert when "
        "notifications are configured.\n\nPlease do not provide sensitive medical "
        "or health information through public website forms.",
    ),
    (
        "privacy_choices",
        "",
        "Your choices",
        "You may ask us to correct or delete details submitted through this website, "
        "subject to applicable record-keeping needs. Contact us using the email "
        "address below with your request.\n\nSpam detection fields help protect the "
        "website from automated submissions and are not used for marketing.",
    ),
]


def add_privacy_and_form_content(apps, schema_editor):
    PageContent = apps.get_model("core", "PageContent")
    SectionContent = apps.get_model("core", "SectionContent")

    PageContent.objects.update_or_create(
        slug="privacy",
        defaults={
            "title": "Privacy Notice",
            "meta_title": "Privacy Notice | Health Planet Foundation",
            "hero_class": "hero-contact",
            "hero_kicker": "Privacy notice",
            "hero_title": "Your information deserves careful handling.",
            "hero_text": (
                "This notice explains what we collect through the website and how "
                "to contact us about your information."
            ),
            "static_image": "images/im-18.jpeg",
            "image_alt": "Your information deserves careful handling.",
        },
    )
    SectionContent.objects.update_or_create(
        page_slug="donate",
        key="donate_details",
        defaults={"body": DONATE_BODY},
    )
    for key, kicker, title, body in PRIVACY_SECTIONS:
        SectionContent.objects.update_or_create(
            page_slug="privacy",
            key=key,
            defaults={"kicker": kicker, "title": title, "body": body},
        )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_replace_tawanda_with_sibeso"),
    ]

    operations = [
        migrations.RunPython(add_privacy_and_form_content, migrations.RunPython.noop),
    ]
