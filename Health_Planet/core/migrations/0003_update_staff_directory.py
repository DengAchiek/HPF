from django.db import migrations


TEAM_MEMBERS = [
    (
        "management",
        "Doreen McGeachy",
        "Executive Director",
        "Masters candidate for Public Health; degree in Public Health. Over 15 years of experience in the NGO and Health sectors with expertise in project programming and implementation.",
        "",
        "images/staff/doreen-mcgeachy.jpg",
        False,
        10,
    ),
    (
        "management",
        "Maureen Nyambe",
        "Technical Advisor",
        "Holds a Masters degree in Public Health. Over 20 years of experience in the NGO and Health sectors with significant expertise in technical advising, project programming and implementation.",
        "",
        "images/staff/maureen-nyambe.jpg",
        False,
        20,
    ),
    (
        "management",
        "Nolia Chipundo",
        "Programs Manager",
        "Holds an MSc in Project Management and CA Zambia qualification. Brings over 5 years of project management experience and over 10 years of financial expertise across the non-profit, private, and government sectors.",
        "",
        "images/staff/nolia-chipundo.jpg",
        False,
        30,
    ),
    (
        "management",
        "Mercy Chipundo",
        "Finance & Administration Manager",
        "An accountant with over 10 years of experience managing organizational budgets and workplans. Holds a Diploma in Accountancy.",
        "",
        "images/staff/mercy-chipundo.jpg",
        False,
        40,
    ),
    (
        "board",
        "Liyoka Liyoka",
        "Chairperson",
        "A dedicated development practitioner with over 15 years of experience in community health, youth empowerment, and climate resilience. Known for strong leadership and collaborative skills.",
        "",
        "images/staff/liyoka-liyoka.jpg",
        False,
        10,
    ),
    (
        "board",
        "Yapoma Nkhoma",
        "Board Secretary",
        "A seasoned professional with over 25 years of experience in pharmacy, public health logistics, and supply chain management. Holds DipPharm, BPharm, MSc in Procurement & Logistics, and LLB.",
        "",
        "images/staff/yapoma-nkhoma.jpg",
        False,
        20,
    ),
    (
        "board",
        "Bupe Harriet Mutale",
        "Director Finance",
        "Holds qualifications in Economics (BA) and Accounting (ACCA). Over 7 to 10 years of experience in insurance, auditing, and corporate advisory roles.",
        "",
        "images/staff/bupe-harriet-mutale-portrait.jpg",
        False,
        30,
    ),
    (
        "board",
        "Tawanda Nyandoro",
        "Director Human Resources",
        "A seasoned Human Resource and Administration professional with 10 years of progressive experience across FMCG, Logistics, NGO and Banking sectors. Holds a Masters Degree in Human Resource Management from the National Institute of Public Administration (NIPA) and several other professional certifications.",
        "",
        "images/staff/tawanda-nyandoro.jpg",
        False,
        40,
    ),
    (
        "board",
        "Dr. Gladys Muyembe",
        "Director Programs",
        "A dental and public health specialist with more than 15 years of professional experience. Holds expertise in public health programming and serves as Vice President of the Zambia Dental Association (ZDA).",
        "",
        "images/staff/gladys-muyembe.jpg",
        False,
        50,
    ),
    (
        "board",
        "Salome Sichali",
        "Director Advocacy & Health Promotions",
        "A senior development professional with over 20 years of experience in governance, gender integration, civil society strengthening, and strategic partnerships. Holds a BA in Development Studies.",
        "",
        "images/staff/salome-sichali.jpg",
        False,
        60,
    ),
    (
        "board",
        "Lujenda Kholoma",
        "Director Monitoring & Evaluation",
        "An M&E and public health professional with over a decade of experience. Holds an MPH in Population Studies & Global Health, Postgraduate Diploma in M&E, and BA in Demography and Development Studies.",
        "",
        "images/staff/lujenda-kholoma-portrait.jpg",
        False,
        70,
    ),
]


def update_staff_directory(apps, schema_editor):
    TeamMember = apps.get_model("core", "TeamMember")
    for team, name, role, bio, initials, static_photo, photo_pending, sort_order in TEAM_MEMBERS:
        TeamMember.objects.update_or_create(
            name=name,
            defaults={
                "team": team,
                "role": role,
                "bio": bio,
                "initials": initials,
                "static_photo": static_photo,
                "photo_alt": name,
                "photo_pending": photo_pending,
                "sort_order": sort_order,
                "is_active": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_seed_site_content"),
    ]

    operations = [
        migrations.RunPython(update_staff_directory, migrations.RunPython.noop),
    ]
