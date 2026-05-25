from django.db import migrations


SIBESO_PROFILE = {
    "team": "board",
    "name": "Sibeso",
    "role": "Director Human Resources",
    "bio": (
        "Sibeso is an accomplished Human Resources Manager with over 7 years of "
        "professional work experience spanning human resources administration, "
        "talent acquisition, and labor relations. Her academic qualifications "
        "include a Master's Degree in Employment and Labor Law from the University "
        "of Lusaka, a Bachelor's Degree in Cultural Anthropology from the University "
        "of Zambia, and both a Diploma and a Certificate in Human Resource Management "
        "from the National Institute of Public Administration. She is currently "
        "working as Human Resources Manager at Opputune Time Business Consultants."
    ),
    "initials": "",
    "photo": "",
    "static_photo": "images/staff/sibeso.jpg",
    "photo_alt": "Sibeso",
    "photo_pending": False,
    "sort_order": 40,
    "is_active": True,
}


def replace_tawanda_with_sibeso(apps, schema_editor):
    TeamMember = apps.get_model("core", "TeamMember")
    former_profile = TeamMember.objects.filter(name="Tawanda Nyandoro").first()

    if former_profile is None:
        return

    sibeso_profile = TeamMember.objects.filter(name="Sibeso").exclude(pk=former_profile.pk).first()
    if sibeso_profile:
        former_profile.delete()
    else:
        sibeso_profile = former_profile

    for field, value in SIBESO_PROFILE.items():
        setattr(sibeso_profile, field, value)
    sibeso_profile.save(update_fields=list(SIBESO_PROFILE))


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_newsitem_body_newsitem_slug_newsimage"),
    ]

    operations = [
        migrations.RunPython(replace_tawanda_with_sibeso, migrations.RunPython.noop),
    ]
