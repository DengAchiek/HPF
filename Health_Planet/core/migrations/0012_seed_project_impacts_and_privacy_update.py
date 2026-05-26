from django.db import migrations
from django.utils.text import slugify


PROJECT_IMPACTS = {
    "Climate-Smart Clinics": {
        "slug": "climate-smart-clinics",
        "location": "Lusaka, Zambia",
        "period_label": "Ongoing",
        "body": (
            "Climate pressure can interrupt basic health services at the exact moment "
            "families need them most. Climate-Smart Clinics works with community and "
            "facility teams to identify local risks, protect essential services, and "
            "strengthen practical readiness.\n\nActivities connect preparedness planning "
            "with community health information, water safety, and referral continuity "
            "so local responses remain grounded in everyday needs."
        ),
        "outcomes_text": (
            "Community-led risk mapping and preparedness conversations\n"
            "Practical planning for essential health service continuity\n"
            "Stronger links between household readiness and referral pathways"
        ),
        "images": [
            ("images/im-13.jpeg", "Team members preparing field materials", "Preparedness planning", 10),
            ("images/im-15.jpeg", "Program staff arranging community health supplies", "Readiness materials", 20),
        ],
    },
    "Safe Motherhood Circles": {
        "slug": "safe-motherhood-circles",
        "location": "Lusaka, Zambia",
        "period_label": "Ongoing",
        "body": (
            "Safe Motherhood Circles create welcoming spaces for families to receive "
            "trustworthy maternal and reproductive health information close to home. "
            "Community sessions focus on respectful listening, early referral, and "
            "reducing barriers to seeking care.\n\nWorking with local partners helps "
            "families recognise concerns early and connect with appropriate services "
            "while preserving dignity and trust."
        ),
        "outcomes_text": (
            "Trusted maternal health conversations in community settings\n"
            "Earlier referral awareness for mothers and families\n"
            "Peer support that strengthens confidence in accessing care"
        ),
        "images": [
            ("images/im-17.jpeg", "Mothers and health volunteers in session", "Community circle", 10),
            ("images/im-18.jpeg", "Community health conversation", "Trusted support", 20),
        ],
    },
    "Youth Mental Wellness": {
        "slug": "youth-mental-wellness",
        "location": "Lusaka, Zambia",
        "period_label": "Ongoing",
        "body": (
            "Young people need safe, respectful opportunities to talk about emotional "
            "wellbeing and understand where support can be found. Youth Mental Wellness "
            "supports age-appropriate community conversations that reduce stigma and "
            "promote earlier help-seeking.\n\nThe program works through youth-friendly "
            "outreach, trusted facilitators, and referral information that can connect "
            "awareness with real support."
        ),
        "outcomes_text": (
            "Youth-friendly mental wellness conversations\n"
            "Reduced stigma through trusted community outreach\n"
            "Clearer pathways for seeking additional support"
        ),
        "images": [
            ("images/im-19.jpeg", "Young people gathered outdoors", "Youth outreach", 10),
            ("images/im-01.jpeg", "Community gathering for a session", "Wellness dialogue", 20),
        ],
    },
}

PRIVACY_UPDATES = {
    "privacy_intro": {
        "kicker": "Last updated: 26 May 2026",
    },
    "privacy_information": {
        "body": (
            "When you use the contact form, we collect your name, email address, "
            "optional phone and organization details, and your message.\n\nWhen you "
            "submit donation interest, we collect your contact details, preferred "
            "contribution amount, and any note you provide. This form does not collect "
            "card, mobile money, or bank payment details.\n\nWhen you apply for a role "
            "or internship, we collect your contact details, selected opportunity, "
            "motivation, and an optional CV or portfolio link that you choose to share."
        ),
    },
    "privacy_use": {
        "body": (
            "We use submissions to answer enquiries, discuss partnerships, follow up "
            "about voluntary support, and review applications. Authorized staff may "
            "review submissions in the website administration system and may receive "
            "an email alert when notifications are configured.\n\nOptional website "
            "analytics only loads after a visitor allows analytics in the on-screen "
            "preference prompt and an administrator has configured a measurement ID.\n\n"
            "Please do not provide sensitive medical or health information through "
            "public website forms."
        ),
    },
    "privacy_choices": {
        "body": (
            "You may ask us to correct or delete details submitted through this website, "
            "subject to applicable record-keeping needs. Contact us using the email "
            "address below with your request.\n\nSpam detection fields help protect the "
            "website from automated submissions and are not used for marketing. Your "
            "analytics choice is stored in your browser and analytics is not loaded "
            "when you decline."
        ),
    },
}


def seed_project_impacts_and_privacy(apps, schema_editor):
    PageContent = apps.get_model("core", "PageContent")
    Project = apps.get_model("core", "Project")
    ProjectImage = apps.get_model("core", "ProjectImage")
    SectionContent = apps.get_model("core", "SectionContent")

    for page in PageContent.objects.filter(meta_description=""):
        page.meta_description = page.hero_text[:280]
        page.save(update_fields=["meta_description"])

    for title, content in PROJECT_IMPACTS.items():
        project = Project.objects.filter(title=title).first()
        if not project:
            continue
        for field in ("slug", "location", "period_label", "body", "outcomes_text"):
            setattr(project, field, content[field])
        project.save(update_fields=["slug", "location", "period_label", "body", "outcomes_text"])
        for static_image, image_alt, caption, sort_order in content["images"]:
            ProjectImage.objects.update_or_create(
                project=project,
                static_image=static_image,
                defaults={
                    "image_alt": image_alt,
                    "caption": caption,
                    "sort_order": sort_order,
                    "is_active": True,
                },
            )

    used_slugs = set(
        Project.objects.exclude(slug__isnull=True).exclude(slug="").values_list("slug", flat=True)
    )
    for project in Project.objects.filter(slug__isnull=True) | Project.objects.filter(slug=""):
        base_slug = slugify(project.title)[:180] or "project"
        slug = base_slug
        counter = 2
        while slug in used_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        project.slug = slug
        project.save(update_fields=["slug"])
        used_slugs.add(slug)

    for key, values in PRIVACY_UPDATES.items():
        SectionContent.objects.filter(page_slug="privacy", key=key).update(**values)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_pagecontent_meta_description_project_body_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_project_impacts_and_privacy, migrations.RunPython.noop),
    ]
