from django.db import migrations


def upsert(model, lookup, defaults):
    model.objects.update_or_create(**lookup, defaults=defaults)


def seed_content(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    NavigationItem = apps.get_model("core", "NavigationItem")
    FooterLink = apps.get_model("core", "FooterLink")
    PageContent = apps.get_model("core", "PageContent")
    SectionContent = apps.get_model("core", "SectionContent")
    FeatureCard = apps.get_model("core", "FeatureCard")
    StatItem = apps.get_model("core", "StatItem")
    Project = apps.get_model("core", "Project")
    NewsItem = apps.get_model("core", "NewsItem")
    GalleryImage = apps.get_model("core", "GalleryImage")
    TeamMember = apps.get_model("core", "TeamMember")
    FocusArea = apps.get_model("core", "FocusArea")
    CareerOpening = apps.get_model("core", "CareerOpening")
    InternshipTrack = apps.get_model("core", "InternshipTrack")
    DonationAmount = apps.get_model("core", "DonationAmount")

    upsert(
        SiteSettings,
        {"singleton_key": "main"},
        {
            "organization_name": "Health Planet Foundation",
            "tagline": "Sustainable environment, Healthy communities, Future generations",
            "footer_about": "Building healthier, more resilient communities through climate readiness, maternal health, youth wellness, and trusted local partnerships.",
            "focus_dropdown_label": "Focus Areas",
            "static_logo": "images/HPF-logo.jpeg",
            "contact_name": "Healthy Planet Foundation Zambia",
            "location": "Lusaka, Zambia",
            "email": "healthyplanetfoundation@gmail.com",
            "phone": "+260971693902",
            "copyright_text": "© 2026 Health Planet Foundation. All rights reserved.",
        },
    )

    for item in [
        ("Home", "home", 10, False),
        ("About", "about", 20, False),
        ("Projects", "projects", 30, False),
        ("News", "news", 50, False),
        ("Careers", "careers", 60, False),
        ("Internships", "internships", 70, False),
        ("Contact", "contact", 80, False),
        ("Donate", "donate", 90, True),
    ]:
        label, url_name, sort_order, is_cta = item
        upsert(
            NavigationItem,
            {"url_name": url_name, "is_cta": is_cta},
            {"label": label, "sort_order": sort_order, "is_active": True, "external_url": ""},
        )

    footer_links = [
        ("programs", "Climate resilience", "projects", "", 10),
        ("programs", "Safe motherhood", "projects", "", 20),
        ("programs", "Mental wellness", "projects", "", 30),
        ("organization", "About", "about", "", 10),
        ("organization", "Careers", "careers", "", 20),
        ("organization", "Internships", "internships", "", 30),
        ("contact", "Partner with us", "contact", "", 10),
        ("contact", "Donate", "donate", "", 20),
    ]
    for group, label, url_name, external_url, sort_order in footer_links:
        upsert(
            FooterLink,
            {"group": group, "label": label},
            {
                "url_name": url_name,
                "external_url": external_url,
                "sort_order": sort_order,
                "is_active": True,
            },
        )

    pages = [
        (
            "home",
            "Home",
            "Health Planet Foundation | Community Resilience",
            "",
            "Health, climate, and dignity",
            "Health Planet Foundation",
            "Helping communities prepare for climate risk while strengthening maternal health, youth wellness, and trusted public health action.",
            "images/im-01.jpeg",
        ),
        (
            "about",
            "About",
            "About | Health Planet Foundation",
            "hero-about",
            "About us",
            "Community health gets stronger when climate realities are part of the plan.",
            "Health Planet Foundation brings public health workers, youth leaders, mothers, and community partners together around practical action.",
            "images/im-09.jpeg",
        ),
        (
            "projects",
            "Projects",
            "Projects | Health Planet Foundation",
            "hero-projects",
            "Projects",
            "Programs designed for health systems, families, and young people.",
            "Our projects focus on prevention, preparedness, and trusted community support.",
            "images/im-13.jpeg",
        ),
        (
            "focus_area",
            "Focus Area",
            "Focus Area | Health Planet Foundation",
            "hero-focus",
            "Focus area",
            "Focus areas that strengthen community health readiness.",
            "Work with Health Planet Foundation to strengthen community health readiness.",
            "images/im-05.jpeg",
        ),
        (
            "news",
            "News",
            "News | Health Planet Foundation",
            "hero-news",
            "News",
            "Field notes, program updates, and partner stories.",
            "Follow the work as community teams strengthen health and climate resilience.",
            "images/im-17.jpeg",
        ),
        (
            "careers",
            "Careers",
            "Careers | Health Planet Foundation",
            "hero-careers",
            "Careers",
            "Work with a team focused on practical community health impact.",
            "We look for people who listen carefully, move with integrity, and care about the details that make programs last.",
            "images/im-19.jpeg",
        ),
        (
            "internships",
            "Internships",
            "Internships | Health Planet Foundation",
            "hero-internships",
            "Internships",
            "Learn by supporting real public health and climate resilience work.",
            "Interns contribute to field preparation, communications, research, and program reporting.",
            "images/im-16.jpeg",
        ),
        (
            "donate",
            "Donate",
            "Donate | Health Planet Foundation",
            "hero-donate",
            "Donate",
            "Your support helps communities prepare earlier and care better.",
            "Contributions support training, community sessions, field materials, and referral coordination.",
            "images/im-15.jpeg",
        ),
        (
            "contact",
            "Contact",
            "Contact | Health Planet Foundation",
            "hero-contact",
            "Contact",
            "Start a partnership conversation or reach the program team.",
            "Tell us what you are working on and where collaboration could help.",
            "images/im-18.jpeg",
        ),
    ]
    for slug, title, meta_title, hero_class, kicker, hero_title, hero_text, static_image in pages:
        upsert(
            PageContent,
            {"slug": slug},
            {
                "title": title,
                "meta_title": meta_title,
                "hero_class": hero_class,
                "hero_kicker": kicker,
                "hero_title": hero_title,
                "hero_text": hero_text,
                "static_image": static_image,
                "image_alt": hero_title,
            },
        )

    sections = [
        ("home", "home_hero_primary", "", "", "", "", "", "", "Explore programs", "projects"),
        ("home", "home_hero_secondary", "", "", "", "", "", "", "Support the work", "donate"),
        ("home", "home_features", "", "What we do", "Community programs built around prevention, preparedness, and care people can actually reach.", "", "", "", "", ""),
        ("home", "home_why", "Why it matters", "Prepared communities, healthier families", "Climate pressure is already changing how families access safe water, maternal care, mental health support, and reliable health information. Our work connects those needs through practical community-led action.", "images/im-12.jpeg", "Health Planet Foundation team member supporting a community health activity", "Community readiness in practice", "Learn more", "about"),
        ("home", "home_gallery", "", "Community work in action", "Real moments from outreach, demonstrations, field preparation, and community health conversations.", "", "", "", "", ""),
        ("home", "home_projects", "", "Current projects", "Each project is designed with community partners and grounded in practical, local action.", "", "", "", "", ""),
        ("home", "home_updates", "", "Updates from community teams", "Stories from volunteers, district teams, and young leaders working across health and climate priorities.", "", "", "", "", ""),
        ("home", "home_cta", "Get involved", "Help communities stay prepared, supported, and healthy.", "", "", "", "", "Start a partnership", "contact"),
        ("about", "about_purpose", "Our purpose", "Prepared communities, healthier families", "We work at the point where climate pressure meets everyday health. That means helping communities prepare for heat and floods, supporting safe motherhood, improving mental wellness, and making reliable health information easier to reach.\n\nOur approach is local, collaborative, and practical. We listen first, build with partners, and focus on tools that communities can keep using long after a project launch.", "", "", "", "", ""),
        ("about", "about_field", "Field presence", "Support that meets people where they are.", "From homes and clinics to outdoor community meetings, our work is built around trust, listening, and practical health support.", "", "", "", "", ""),
        ("about", "about_work", "", "How we work", "Monoline-inspired clarity, Health Planet substance: clean, direct, and grounded in community trust.", "", "", "", "", ""),
        ("about", "about_team", "Our team", "Leadership and governance", "Meet the people guiding Health Planet Foundation through community health, climate resilience, public health programming, finance, advocacy, and organizational growth.", "", "", "", "", ""),
        ("projects", "projects_list", "", "Current programs", "Field-ready work shaped by partners, public health teams, and community leaders.", "", "", "", "", ""),
        ("news", "news_list", "", "Latest updates", "Short reads from the field and from the teams supporting community health work.", "", "", "", "", ""),
        ("careers", "careers_intro", "Team culture", "Work close to the communities we serve.", "Our team values respectful field practice, clear reporting, and patient relationship-building with partners and families.", "images/im-19.jpeg", "Health Planet Foundation staff and community members gathered outdoors", "Community-centered work", "", ""),
        ("careers", "careers_roles", "", "Open roles", "Join field-aware work across programs, learning, communications, and partner support.", "", "", "", "", ""),
        ("internships", "internships_intro", "Hands-on learning", "Support field work, storytelling, and program preparation.", "Interns help prepare sessions, document community needs, and learn how public health programs move from planning to practice.", "images/im-16.jpeg", "Intern supporting a community health activity", "Learning through service", "", ""),
        ("internships", "internships_tracks", "", "Internship tracks", "Designed for emerging professionals who want practical experience with community-centered programs.", "", "", "", "", ""),
        ("donate", "donate_details", "Support the mission", "Choose an amount", "This demo form records your interest locally and can be connected to a payment provider when the organization is ready.", "images/im-15.jpeg", "Program staff preparing community health materials", "", "", ""),
        ("contact", "contact_details", "Reach us", "Program office", "", "images/im-18.jpeg", "Health Planet Foundation team speaking with community members", "", "", ""),
        ("contact", "contact_note", "", "Partnership focus", "Community health, climate resilience, safe motherhood, mental wellness, and youth-centered public health programs.", "", "", "", "", ""),
        ("focus_area", "focus_cta", "Focus areas", "Work with Health Planet Foundation to strengthen community health readiness.", "", "", "", "", "Explore projects", "projects"),
    ]
    for page_slug, key, kicker, title, body, static_image, image_alt, caption, button_label, button_url_name in sections:
        upsert(
            SectionContent,
            {"page_slug": page_slug, "key": key},
            {
                "kicker": kicker,
                "title": title,
                "body": body,
                "static_image": static_image,
                "image_alt": image_alt,
                "image_caption": caption,
                "button_label": button_label,
                "button_url_name": button_url_name,
                "button_external_url": "",
            },
        )

    feature_cards = [
        ("home_features", "01", "Climate Resilience", "Local planning tools for heat, flooding, water safety, and continuity of essential health services.", 10),
        ("home_features", "02", "Safe Motherhood", "Peer circles, trusted health information, and referral support for expectant mothers and families.", 20),
        ("home_features", "03", "Mental Health", "Community conversations that reduce stigma and help people seek support earlier.", 30),
        ("home_features", "04", "SRH Awareness", "Youth-centered education for informed decisions, safer pathways, and stronger futures.", 40),
        ("home_impact_points", "", "Early planning", "", 10),
        ("home_impact_points", "", "Trusted referrals", "", 20),
        ("home_impact_points", "", "Local leadership", "", 30),
        ("about_work", "01", "Built with communities", "Programs are shaped with the people closest to the needs, risks, and solutions.", 10),
        ("about_work", "02", "Practical over abstract", "We favor tools, training, and referrals that can be used in daily community health work.", 20),
        ("about_work", "03", "Care without stigma", "Maternal health, mental wellness, and youth health deserve privacy, respect, and trust.", 30),
    ]
    for section_key, icon, title, body, sort_order in feature_cards:
        upsert(
            FeatureCard,
            {"section_key": section_key, "title": title},
            {"icon": icon, "body": body, "sort_order": sort_order, "is_active": True},
        )

    for label, value, description, sort_order in [
        ("Focus areas", "4", "Integrated public health priorities", 10),
        ("Partners", "12+", "Community and district collaborators", 20),
        ("Programs", "3", "Current projects in motion", 30),
        ("Year", "2026", "Expansion and learning cycle", 40),
    ]:
        upsert(StatItem, {"label": label}, {"value": value, "description": description, "sort_order": sort_order, "is_active": True})

    projects = [
        ("Climate-Smart Clinics", "Helping rural health posts prepare for heat, flooding, and service disruption through local planning and practical resilience tools.", "Active", "images/im-13.jpeg", "Health Planet Foundation team members preparing field materials", 10),
        ("Safe Motherhood Circles", "Community-led sessions connecting expectant mothers with health information, referral support, and trusted peer networks.", "Field program", "images/im-17.jpeg", "Community session with mothers and health volunteers", 20),
        ("Youth Mental Wellness", "School and community outreach that makes mental health conversations easier, earlier, and connected to local care pathways.", "Growing", "images/im-19.jpeg", "Young people and community leaders gathering outdoors", 30),
    ]
    for title, description, status, static_image, image_alt, sort_order in projects:
        upsert(Project, {"title": title}, {"description": description, "status": status, "static_image": static_image, "image_alt": image_alt, "sort_order": sort_order, "is_active": True})

    news = [
        ("Community health volunteers expand outreach in Lusaka Province", "May 2026", "New volunteer cohorts are supporting health talks, referrals, and preparedness conversations in high-risk communities.", "images/im-09.jpeg", "Community members attending a Health Planet Foundation outreach session", 10),
        ("Climate resilience sessions reach district health teams", "April 2026", "District teams reviewed practical response plans for heat stress, water safety, and continuity of essential services.", "images/im-08.jpeg", "Field preparation work at a community site", 20),
        ("Youth wellness clubs launch a peer-support calendar", "March 2026", "Young leaders are creating consistent spaces for mental wellness education and early help-seeking.", "images/im-01.jpeg", "Youth and community members seated during an outdoor session", 30),
    ]
    for title, date_label, summary, static_image, image_alt, sort_order in news:
        upsert(NewsItem, {"title": title}, {"date_label": date_label, "summary": summary, "static_image": static_image, "image_alt": image_alt, "sort_order": sort_order, "is_active": True})

    gallery = [
        ("home_gallery", "images/im-01.jpeg", "Community members gathered outdoors for a Health Planet Foundation session", "Outdoor health talk", "focus-center", 10),
        ("home_gallery", "images/im-02.jpeg", "Community group gathered for a health discussion", "Community dialogue", "focus-center", 20),
        ("home_gallery", "images/im-03.jpeg", "Health Planet Foundation volunteers speaking with community members", "Field outreach", "focus-upper", 30),
        ("home_gallery", "images/im-04.jpeg", "Volunteer supporting a household health activity", "Household support", "focus-upper", 40),
        ("home_gallery", "images/im-05.jpeg", "Team member demonstrating handwashing and water safety materials", "Practical demos", "focus-upper", 50),
        ("home_gallery", "images/im-06.jpeg", "Children and adults gathered under a tree for community programming", "Local participation", "focus-upper", 60),
        ("home_gallery", "images/im-07.jpeg", "Community members receiving support during an outdoor session", "Trusted presence", "focus-upper", 70),
        ("home_gallery", "images/im-08.jpeg", "Field preparation work at a community site", "Site preparation", "focus-center", 80),
        ("home_gallery", "images/im-09.jpeg", "Community members waiting during a Health Planet Foundation outreach day", "Outreach day", "focus-center", 90),
        ("home_gallery", "images/im-10.jpeg", "Health Planet Foundation staff member speaking with a mother during a home visit", "Home visit", "focus-upper", 100),
        ("home_gallery", "images/im-11.jpeg", "Team member holding program supplies for community outreach", "Program supplies", "focus-center", 110),
        ("home_gallery", "images/im-12.jpeg", "Health Planet Foundation team member supporting a community health activity", "Hands-on support", "focus-center", 120),
        ("home_gallery", "images/im-13.jpeg", "Health Planet Foundation team with field materials", "Prepared teams", "focus-center", 130),
        ("home_gallery", "images/im-14.jpeg", "Health Planet Foundation team with field supplies", "Field supplies", "focus-center", 140),
        ("home_gallery", "images/im-15.jpeg", "Program staff arranging community health supplies", "Field materials", "focus-center", 150),
        ("home_gallery", "images/im-16.jpeg", "Intern supporting a community health activity", "Learning through service", "focus-upper", 160),
        ("home_gallery", "images/im-17.jpeg", "Community session with mothers and health volunteers", "Motherhood circle", "focus-center", 170),
        ("home_gallery", "images/im-18.jpeg", "Health Planet Foundation team speaking with community members", "Community meeting", "focus-center", 180),
        ("home_gallery", "images/im-19.jpeg", "Young people and community leaders gathering outdoors", "Youth engagement", "focus-upper", 190),
        ("home_gallery", "images/im-20.jpeg", "Health Planet Foundation volunteer supporting bedside care", "Care support", "focus-upper", 200),
        ("about_slideshow", "images/im-10.jpeg", "Health Planet Foundation staff member speaking with a mother during a home visit", "Home-based community health support", "", 10),
        ("about_slideshow", "images/im-11.jpeg", "Team member holding program materials for community outreach", "Prepared outreach teams and supplies", "", 20),
        ("about_slideshow", "images/im-20.jpeg", "Health Planet Foundation volunteer supporting bedside care", "Trusted support for families", "", 30),
    ]
    for gallery_key, static_image, image_alt, caption, focus_class, sort_order in gallery:
        upsert(GalleryImage, {"gallery_key": gallery_key, "static_image": static_image}, {"image_alt": image_alt, "caption": caption, "focus_class": focus_class, "sort_order": sort_order, "is_active": True})

    team = [
        ("management", "Doreen McGeachy", "Executive Director", "Masters candidate for Public Health with a degree in Public Health. She brings over 15 years of NGO and health sector experience in project programming and implementation.", "", "images/staff/doreen-mcgeachy.jpg", False, 10),
        ("management", "Maureen Nyambe", "Technical Advisor", "Holds a Masters degree in Public Health and has over 20 years of NGO and health sector experience, with deep expertise in technical advising and project implementation.", "", "images/staff/maureen-nyambe.jpg", False, 20),
        ("management", "Nolia Chipundo", "Programs Manager", "Holds an MSc in Project Management from ZCAS University and a CA Zambia qualification, with over 5 years in project management and over 10 years of financial expertise.", "", "images/staff/nolia-chipundo.jpg", False, 30),
        ("management", "Mercy Chipundo", "Finance & Administration Manager", "An accountant with over 10 years of experience managing organizational budgets and workplans. She holds a Diploma from the University of Zambia.", "", "images/staff/mercy-chipundo.jpg", False, 40),
        ("board", "Liyoka Liyoka", "Chairperson", "A dedicated development practitioner with over 15 years of experience in community health, youth empowerment, and climate resilience, known for strong leadership and collaboration.", "LL", "", True, 10),
        ("board", "Yapoma Nkhoma", "Board Secretary", "A seasoned professional with over 25 years of experience in pharmacy, public health logistics, and supply chain management. Holds DipPharm, BPharm, MSc in Procurement & Logistics, and LLB.", "", "images/staff/yapoma-nkhoma.jpg", False, 20),
        ("board", "Bupe Harriet Mutale", "Director Finance", "Holds qualifications in Economics from Mulungushi University and Accounting through ACCA, with 7 to 10 years of experience in insurance, auditing, and corporate advisory roles.", "", "images/staff/bupe-harriet-mutale-portrait.jpg", False, 30),
        ("board", "Tawanda Nyandoro", "Director Human Resources", "Currently Manager, People & Culture Business Partnering at Access Bank Zambia, with over 10 years of HR experience across FMCG, logistics, NGOs, and banking.", "TN", "", True, 40),
        ("board", "Dr. Gladys Muyembe", "Director Programs", "A dental and public health specialist with more than 15 years of professional experience. She serves as a Public Health Specialist at the Ministry of Health Zambia.", "", "images/staff/gladys-muyembe.jpg", False, 50),
        ("board", "Salome Sichali", "Director Advocacy & Health Promotions", "A senior development professional with over 20 years of experience in governance, gender integration, civil society strengthening, and strategic partnerships.", "", "images/staff/salome-sichali.jpg", False, 60),
        ("board", "Lujenda Kholoma", "Director Monitoring & Evaluation", "An M&E and public health professional with over a decade of experience. Holds an MPH in Population Studies & Global Health, a Postgraduate Diploma in M&E, and a BA in Demography and Development Studies.", "", "images/staff/lujenda-kholoma-portrait.jpg", False, 70),
    ]
    for team_name, name, role, bio, initials, static_photo, photo_pending, sort_order in team:
        upsert(TeamMember, {"name": name}, {"team": team_name, "role": role, "bio": bio, "initials": initials, "static_photo": static_photo, "photo_alt": name, "photo_pending": photo_pending, "sort_order": sort_order, "is_active": True})

    focus_areas = [
        ("epidemic-preparedness", "Epidemic Preparedness", "Helping communities recognize risks early, prepare local response pathways, and keep essential health information moving during outbreaks.", "images/im-04.jpeg", "Volunteer supporting a household health activity", "Community readiness sessions\nEarly-warning communication\nReferral and response coordination", 10),
        ("advocacy-and-health-promotions", "Advocacy and Health Promotions", "Supporting health education, public awareness, and trusted community conversations that help families act earlier and make informed choices.", "images/im-09.jpeg", "Community members attending a Health Planet Foundation outreach session", "Health talks and campaigns\nYouth-centered awareness\nCommunity-led advocacy", 20),
        ("wash", "WASH", "Promoting practical water, sanitation, and hygiene action so families can reduce preventable health risks in everyday life.", "images/im-15.jpeg", "Program staff arranging WASH and community health supplies", "Water safety demonstrations\nHygiene promotion\nHousehold sanitation support", 30),
    ]
    for slug, title, summary, static_image, image_alt, points_text, sort_order in focus_areas:
        upsert(FocusArea, {"slug": slug}, {"title": title, "kicker": "Focus area", "summary": summary, "static_image": static_image, "image_alt": image_alt, "priority_kicker": "Program priority", "priority_title": "Practical action built around community needs.", "points_text": points_text, "sort_order": sort_order, "is_active": True})

    for role, location, employment_type, sort_order in [
        ("Community Programs Coordinator", "Lusaka, Zambia", "Full time", 10),
        ("Monitoring and Learning Assistant", "Hybrid", "Contract", 20),
    ]:
        upsert(CareerOpening, {"role": role}, {"location": location, "employment_type": employment_type, "sort_order": sort_order, "is_active": True})

    for role, focus, sort_order in [
        ("Communications Intern", "Storytelling, campaigns, and partner updates", 10),
        ("Public Health Intern", "Field research, community sessions, and reporting support", 20),
    ]:
        upsert(InternshipTrack, {"role": role}, {"focus": focus, "icon": "IN", "sort_order": sort_order, "is_active": True})

    for amount, label, select_value, sort_order in [
        ("25", "Field materials", "25", 10),
        ("50", "Community session support", "50", 20),
        ("100", "Training contribution", "100", 30),
    ]:
        upsert(DonationAmount, {"select_value": select_value}, {"amount": amount, "label": label, "sort_order": sort_order, "is_active": True})


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_content, migrations.RunPython.noop),
    ]
