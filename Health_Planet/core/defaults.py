from types import SimpleNamespace

from django.templatetags.static import static


ROUTES = {
    "home": "/",
    "about": "/about/",
    "projects": "/projects/",
    "news": "/news/",
    "careers": "/careers/",
    "internships": "/internships/",
    "donate": "/donate/",
    "contact": "/contact/",
}


def item(**kwargs):
    return SimpleNamespace(**kwargs)


def image_url(path):
    return static(path) if path else ""


def link_url(url_name="", external_url=""):
    return ROUTES.get(url_name, external_url or "#")


def section(
    page_slug,
    key,
    kicker="",
    title="",
    body="",
    static_image="",
    image_alt="",
    image_caption="",
    button_label="",
    button_url_name="",
    button_external_url="",
):
    return item(
        page_slug=page_slug,
        key=key,
        kicker=kicker,
        title=title,
        body=body,
        static_image=static_image,
        image_alt=image_alt,
        image_caption=image_caption,
        button_label=button_label,
        button_url_name=button_url_name,
        button_external_url=button_external_url,
        button_href=link_url(button_url_name, button_external_url),
        image_url=image_url(static_image),
    )


def page(slug, title, meta_title, hero_class, hero_kicker, hero_title, hero_text, static_image):
    return item(
        slug=slug,
        title=title,
        meta_title=meta_title,
        hero_class=hero_class,
        hero_kicker=hero_kicker,
        hero_title=hero_title,
        hero_text=hero_text,
        static_image=static_image,
        image_alt=hero_title,
        image_url=image_url(static_image),
    )


SITE_SETTINGS = item(
    organization_name="Health Planet Foundation",
    tagline="Sustainable environment, Healthy communities, Future generations",
    footer_about="Building healthier, more resilient communities through climate readiness, maternal health, youth wellness, and trusted local partnerships.",
    focus_dropdown_label="Focus Areas",
    contact_name="Healthy Planet Foundation Zambia",
    location="Lusaka, Zambia",
    email="healthyplanetfoundation@gmail.com",
    phone="+260971693902",
    copyright_text="\u00a9 2026 Health Planet Foundation. All rights reserved.",
    logo_url=image_url("images/HPF-logo.jpeg"),
)

NAVIGATION_BEFORE_FOCUS = [
    item(label="Home", url_name="home", href="/", sort_order=10),
    item(label="About", url_name="about", href="/about/", sort_order=20),
    item(label="Projects", url_name="projects", href="/projects/", sort_order=30),
]

NAVIGATION_AFTER_FOCUS = [
    item(label="News", url_name="news", href="/news/", sort_order=50),
    item(label="Careers", url_name="careers", href="/careers/", sort_order=60),
    item(label="Internships", url_name="internships", href="/internships/", sort_order=70),
    item(label="Contact", url_name="contact", href="/contact/", sort_order=80),
]

NAVIGATION_CTAS = [
    item(label="Donate", url_name="donate", href="/donate/", sort_order=90),
]

FOOTER_LINKS = {
    "programs": [
        item(label="Climate resilience", href="/projects/"),
        item(label="Safe motherhood", href="/projects/"),
        item(label="Mental wellness", href="/projects/"),
    ],
    "organization": [
        item(label="About", href="/about/"),
        item(label="Careers", href="/careers/"),
        item(label="Internships", href="/internships/"),
    ],
    "contact": [
        item(label="Partner with us", href="/contact/"),
        item(label="Donate", href="/donate/"),
    ],
}

PAGES = {
    "home": page(
        "home",
        "Home",
        "Health Planet Foundation | Community Resilience",
        "",
        "Health, climate, and dignity",
        "Health Planet Foundation",
        "Helping communities prepare for climate risk while strengthening maternal health, youth wellness, and trusted public health action.",
        "images/im-01.jpeg",
    ),
    "about": page(
        "about",
        "About",
        "About | Health Planet Foundation",
        "hero-about",
        "About us",
        "Community health gets stronger when climate realities are part of the plan.",
        "Health Planet Foundation brings public health workers, youth leaders, mothers, and community partners together around practical action.",
        "images/im-09.jpeg",
    ),
    "projects": page(
        "projects",
        "Projects",
        "Projects | Health Planet Foundation",
        "hero-projects",
        "Projects",
        "Programs designed for health systems, families, and young people.",
        "Our projects focus on prevention, preparedness, and trusted community support.",
        "images/im-13.jpeg",
    ),
    "focus_area": page(
        "focus_area",
        "Focus Area",
        "Focus Area | Health Planet Foundation",
        "hero-focus",
        "Focus area",
        "Focus areas that strengthen community health readiness.",
        "Work with Health Planet Foundation to strengthen community health readiness.",
        "images/im-05.jpeg",
    ),
    "news": page(
        "news",
        "News",
        "News | Health Planet Foundation",
        "hero-news",
        "News",
        "Field notes, program updates, and partner stories.",
        "Follow the work as community teams strengthen health and climate resilience.",
        "images/im-17.jpeg",
    ),
    "careers": page(
        "careers",
        "Careers",
        "Careers | Health Planet Foundation",
        "hero-careers",
        "Careers",
        "Work with a team focused on practical community health impact.",
        "We look for people who listen carefully, move with integrity, and care about the details that make programs last.",
        "images/im-19.jpeg",
    ),
    "internships": page(
        "internships",
        "Internships",
        "Internships | Health Planet Foundation",
        "hero-internships",
        "Internships",
        "Learn by supporting real public health and climate resilience work.",
        "Interns contribute to field preparation, communications, research, and program reporting.",
        "images/im-16.jpeg",
    ),
    "donate": page(
        "donate",
        "Donate",
        "Donate | Health Planet Foundation",
        "hero-donate",
        "Donate",
        "Your support helps communities prepare earlier and care better.",
        "Contributions support training, community sessions, field materials, and referral coordination.",
        "images/im-15.jpeg",
    ),
    "contact": page(
        "contact",
        "Contact",
        "Contact | Health Planet Foundation",
        "hero-contact",
        "Contact",
        "Start a partnership conversation or reach the program team.",
        "Tell us what you are working on and where collaboration could help.",
        "images/im-18.jpeg",
    ),
}

SECTION_LIST = [
    section("home", "home_hero_primary", button_label="Explore programs", button_url_name="projects"),
    section("home", "home_hero_secondary", button_label="Support the work", button_url_name="donate"),
    section(
        "home",
        "home_features",
        title="What we do",
        body="Community programs built around prevention, preparedness, and care people can actually reach.",
    ),
    section(
        "home",
        "home_why",
        kicker="Why it matters",
        title="Prepared communities, healthier families",
        body="Climate pressure is already changing how families access safe water, maternal care, mental health support, and reliable health information. Our work connects those needs through practical community-led action.",
        static_image="images/im-12.jpeg",
        image_alt="Health Planet Foundation team member supporting a community health activity",
        image_caption="Community readiness in practice",
        button_label="Learn more",
        button_url_name="about",
    ),
    section(
        "home",
        "home_gallery",
        title="Community work in action",
        body="Real moments from outreach, demonstrations, field preparation, and community health conversations.",
    ),
    section(
        "home",
        "home_projects",
        title="Current projects",
        body="Each project is designed with community partners and grounded in practical, local action.",
    ),
    section(
        "home",
        "home_updates",
        title="Updates from community teams",
        body="Stories from volunteers, district teams, and young leaders working across health and climate priorities.",
    ),
    section(
        "home",
        "home_cta",
        kicker="Get involved",
        title="Help communities stay prepared, supported, and healthy.",
        button_label="Start a partnership",
        button_url_name="contact",
    ),
    section(
        "about",
        "about_purpose",
        kicker="Our purpose",
        title="Prepared communities, healthier families",
        body="We work at the point where climate pressure meets everyday health. That means helping communities prepare for heat and floods, supporting safe motherhood, improving mental wellness, and making reliable health information easier to reach.\n\nOur approach is local, collaborative, and practical. We listen first, build with partners, and focus on tools that communities can keep using long after a project launch.",
    ),
    section(
        "about",
        "about_field",
        kicker="Field presence",
        title="Support that meets people where they are.",
        body="From homes and clinics to outdoor community meetings, our work is built around trust, listening, and practical health support.",
    ),
    section(
        "about",
        "about_work",
        title="How we work",
        body="Monoline-inspired clarity, Health Planet substance: clean, direct, and grounded in community trust.",
    ),
    section(
        "about",
        "about_team",
        kicker="Our team",
        title="Leadership and governance",
        body="Meet the people guiding Health Planet Foundation through community health, climate resilience, public health programming, finance, advocacy, and organizational growth.",
    ),
    section(
        "projects",
        "projects_list",
        title="Current programs",
        body="Field-ready work shaped by partners, public health teams, and community leaders.",
    ),
    section(
        "news",
        "news_list",
        title="Latest updates",
        body="Short reads from the field and from the teams supporting community health work.",
    ),
    section(
        "careers",
        "careers_intro",
        kicker="Team culture",
        title="Work close to the communities we serve.",
        body="Our team values respectful field practice, clear reporting, and patient relationship-building with partners and families.",
        static_image="images/im-19.jpeg",
        image_alt="Health Planet Foundation staff and community members gathered outdoors",
        image_caption="Community-centered work",
    ),
    section(
        "careers",
        "careers_roles",
        title="Open roles",
        body="Join field-aware work across programs, learning, communications, and partner support.",
    ),
    section(
        "internships",
        "internships_intro",
        kicker="Hands-on learning",
        title="Support field work, storytelling, and program preparation.",
        body="Interns help prepare sessions, document community needs, and learn how public health programs move from planning to practice.",
        static_image="images/im-16.jpeg",
        image_alt="Intern supporting a community health activity",
        image_caption="Learning through service",
    ),
    section(
        "internships",
        "internships_tracks",
        title="Internship tracks",
        body="Designed for emerging professionals who want practical experience with community-centered programs.",
    ),
    section(
        "donate",
        "donate_details",
        kicker="Support the mission",
        title="Choose an amount",
        body="This demo form records your interest locally and can be connected to a payment provider when the organization is ready.",
        static_image="images/im-15.jpeg",
        image_alt="Program staff preparing community health materials",
    ),
    section(
        "contact",
        "contact_details",
        kicker="Reach us",
        title="Program office",
        static_image="images/im-18.jpeg",
        image_alt="Health Planet Foundation team speaking with community members",
    ),
    section(
        "contact",
        "contact_note",
        title="Partnership focus",
        body="Community health, climate resilience, safe motherhood, mental wellness, and youth-centered public health programs.",
    ),
    section(
        "focus_area",
        "focus_cta",
        kicker="Focus areas",
        title="Work with Health Planet Foundation to strengthen community health readiness.",
        button_label="Explore projects",
        button_url_name="projects",
    ),
]

SECTIONS = {}
for section_item in SECTION_LIST:
    SECTIONS.setdefault(section_item.page_slug, {})[section_item.key] = section_item

FEATURES = [
    item(icon="01", title="Climate Resilience", body="Local planning tools for heat, flooding, water safety, and continuity of essential health services."),
    item(icon="02", title="Safe Motherhood", body="Peer circles, trusted health information, and referral support for expectant mothers and families."),
    item(icon="03", title="Mental Health", body="Community conversations that reduce stigma and help people seek support earlier."),
    item(icon="04", title="SRH Awareness", body="Youth-centered education for informed decisions, safer pathways, and stronger futures."),
]

IMPACT_POINTS = [
    item(title="Early planning"),
    item(title="Trusted referrals"),
    item(title="Local leadership"),
]

STATS = [
    item(label="Focus areas", value="4", description="Integrated public health priorities"),
    item(label="Partners", value="12+", description="Community and district collaborators"),
    item(label="Programs", value="3", description="Current projects in motion"),
    item(label="Year", value="2026", description="Expansion and learning cycle"),
]

PROJECTS = [
    item(title="Climate-Smart Clinics", description="Helping rural health posts prepare for heat, flooding, and service disruption through local planning and practical resilience tools.", status="Active", image_url=image_url("images/im-13.jpeg"), image_alt="Health Planet Foundation team members preparing field materials"),
    item(title="Safe Motherhood Circles", description="Community-led sessions connecting expectant mothers with health information, referral support, and trusted peer networks.", status="Field program", image_url=image_url("images/im-17.jpeg"), image_alt="Community session with mothers and health volunteers"),
    item(title="Youth Mental Wellness", description="School and community outreach that makes mental health conversations easier, earlier, and connected to local care pathways.", status="Growing", image_url=image_url("images/im-19.jpeg"), image_alt="Young people and community leaders gathering outdoors"),
]

NEWS_ITEMS = [
    item(title="Community health volunteers expand outreach in Lusaka Province", date_label="May 2026", summary="New volunteer cohorts are supporting health talks, referrals, and preparedness conversations in high-risk communities.", image_url=image_url("images/im-09.jpeg"), image_alt="Community members attending a Health Planet Foundation outreach session"),
    item(title="Climate resilience sessions reach district health teams", date_label="April 2026", summary="District teams reviewed practical response plans for heat stress, water safety, and continuity of essential services.", image_url=image_url("images/im-08.jpeg"), image_alt="Field preparation work at a community site"),
    item(title="Youth wellness clubs launch a peer-support calendar", date_label="March 2026", summary="Young leaders are creating consistent spaces for mental wellness education and early help-seeking.", image_url=image_url("images/im-01.jpeg"), image_alt="Youth and community members seated during an outdoor session"),
]

GALLERY_IMAGES = [
    item(image_url=image_url("images/im-01.jpeg"), image_alt="Community members gathered outdoors for a Health Planet Foundation session", caption="Outdoor health talk", focus_class="focus-center"),
    item(image_url=image_url("images/im-02.jpeg"), image_alt="Community group gathered for a health discussion", caption="Community dialogue", focus_class="focus-center"),
    item(image_url=image_url("images/im-03.jpeg"), image_alt="Health Planet Foundation volunteers speaking with community members", caption="Field outreach", focus_class="focus-upper"),
    item(image_url=image_url("images/im-04.jpeg"), image_alt="Volunteer supporting a household health activity", caption="Household support", focus_class="focus-upper"),
    item(image_url=image_url("images/im-05.jpeg"), image_alt="Team member demonstrating handwashing and water safety materials", caption="Practical demos", focus_class="focus-upper"),
    item(image_url=image_url("images/im-06.jpeg"), image_alt="Children and adults gathered under a tree for community programming", caption="Local participation", focus_class="focus-upper"),
    item(image_url=image_url("images/im-07.jpeg"), image_alt="Community members receiving support during an outdoor session", caption="Trusted presence", focus_class="focus-upper"),
    item(image_url=image_url("images/im-08.jpeg"), image_alt="Field preparation work at a community site", caption="Site preparation", focus_class="focus-center"),
    item(image_url=image_url("images/im-09.jpeg"), image_alt="Community members waiting during a Health Planet Foundation outreach day", caption="Outreach day", focus_class="focus-center"),
    item(image_url=image_url("images/im-10.jpeg"), image_alt="Health Planet Foundation staff member speaking with a mother during a home visit", caption="Home visit", focus_class="focus-upper"),
    item(image_url=image_url("images/im-11.jpeg"), image_alt="Team member holding program supplies for community outreach", caption="Program supplies", focus_class="focus-center"),
    item(image_url=image_url("images/im-12.jpeg"), image_alt="Health Planet Foundation team member supporting a community health activity", caption="Hands-on support", focus_class="focus-center"),
    item(image_url=image_url("images/im-13.jpeg"), image_alt="Health Planet Foundation team with field materials", caption="Prepared teams", focus_class="focus-center"),
    item(image_url=image_url("images/im-14.jpeg"), image_alt="Health Planet Foundation team with field supplies", caption="Field supplies", focus_class="focus-center"),
    item(image_url=image_url("images/im-15.jpeg"), image_alt="Program staff arranging community health supplies", caption="Field materials", focus_class="focus-center"),
    item(image_url=image_url("images/im-16.jpeg"), image_alt="Intern supporting a community health activity", caption="Learning through service", focus_class="focus-upper"),
    item(image_url=image_url("images/im-17.jpeg"), image_alt="Community session with mothers and health volunteers", caption="Motherhood circle", focus_class="focus-center"),
    item(image_url=image_url("images/im-18.jpeg"), image_alt="Health Planet Foundation team speaking with community members", caption="Community meeting", focus_class="focus-center"),
    item(image_url=image_url("images/im-19.jpeg"), image_alt="Young people and community leaders gathering outdoors", caption="Youth engagement", focus_class="focus-upper"),
    item(image_url=image_url("images/im-20.jpeg"), image_alt="Health Planet Foundation volunteer supporting bedside care", caption="Care support", focus_class="focus-upper"),
]

ABOUT_SLIDES = [
    item(image_url=image_url("images/im-10.jpeg"), image_alt="Health Planet Foundation staff member speaking with a mother during a home visit", caption="Home-based community health support"),
    item(image_url=image_url("images/im-11.jpeg"), image_alt="Team member holding program materials for community outreach", caption="Prepared outreach teams and supplies"),
    item(image_url=image_url("images/im-20.jpeg"), image_alt="Health Planet Foundation volunteer supporting bedside care", caption="Trusted support for families"),
]

ABOUT_WORK_FEATURES = [
    item(icon="01", title="Built with communities", body="Programs are shaped with the people closest to the needs, risks, and solutions."),
    item(icon="02", title="Practical over abstract", body="We favor tools, training, and referrals that can be used in daily community health work."),
    item(icon="03", title="Care without stigma", body="Maternal health, mental wellness, and youth health deserve privacy, respect, and trust."),
]

def team_member(team, name, role, bio, static_photo="", initials="", photo_pending=False):
    return item(
        team=team,
        name=name,
        role=role,
        bio=bio,
        initials=initials,
        photo_url=image_url(static_photo),
        photo_alt=name,
        photo_pending=photo_pending,
        display_initials=initials or "".join(part[:1] for part in name.split()[:2]).upper(),
    )


MANAGEMENT_TEAM = [
    team_member("management", "Doreen McGeachy", "Executive Director", "Masters candidate for Public Health with a degree in Public Health. She brings over 15 years of NGO and health sector experience in project programming and implementation.", "images/staff/doreen-mcgeachy.jpg"),
    team_member("management", "Maureen Nyambe", "Technical Advisor", "Holds a Masters degree in Public Health and has over 20 years of NGO and health sector experience, with deep expertise in technical advising and project implementation.", "images/staff/maureen-nyambe.jpg"),
    team_member("management", "Nolia Chipundo", "Programs Manager", "Holds an MSc in Project Management from ZCAS University and a CA Zambia qualification, with over 5 years in project management and over 10 years of financial expertise.", "images/staff/nolia-chipundo.jpg"),
    team_member("management", "Mercy Chipundo", "Finance & Administration Manager", "An accountant with over 10 years of experience managing organizational budgets and workplans. She holds a Diploma from the University of Zambia.", "images/staff/mercy-chipundo.jpg"),
]

BOARD_MEMBERS = [
    team_member("board", "Liyoka Liyoka", "Chairperson", "A dedicated development practitioner with over 15 years of experience in community health, youth empowerment, and climate resilience, known for strong leadership and collaboration.", initials="LL", photo_pending=True),
    team_member("board", "Yapoma Nkhoma", "Board Secretary", "A seasoned professional with over 25 years of experience in pharmacy, public health logistics, and supply chain management. Holds DipPharm, BPharm, MSc in Procurement & Logistics, and LLB.", "images/staff/yapoma-nkhoma.jpg"),
    team_member("board", "Bupe Harriet Mutale", "Director Finance", "Holds qualifications in Economics from Mulungushi University and Accounting through ACCA, with 7 to 10 years of experience in insurance, auditing, and corporate advisory roles.", "images/staff/bupe-harriet-mutale-portrait.jpg"),
    team_member("board", "Tawanda Nyandoro", "Director Human Resources", "Currently Manager, People & Culture Business Partnering at Access Bank Zambia, with over 10 years of HR experience across FMCG, logistics, NGOs, and banking.", initials="TN", photo_pending=True),
    team_member("board", "Dr. Gladys Muyembe", "Director Programs", "A dental and public health specialist with more than 15 years of professional experience. She serves as a Public Health Specialist at the Ministry of Health Zambia.", "images/staff/gladys-muyembe.jpg"),
    team_member("board", "Salome Sichali", "Director Advocacy & Health Promotions", "A senior development professional with over 20 years of experience in governance, gender integration, civil society strengthening, and strategic partnerships.", "images/staff/salome-sichali.jpg"),
    team_member("board", "Lujenda Kholoma", "Director Monitoring & Evaluation", "An M&E and public health professional with over a decade of experience. Holds an MPH in Population Studies & Global Health, a Postgraduate Diploma in M&E, and a BA in Demography and Development Studies.", "images/staff/lujenda-kholoma-portrait.jpg"),
]

FOCUS_AREAS = {
    "epidemic-preparedness": item(slug="epidemic-preparedness", title="Epidemic Preparedness", kicker="Focus area", summary="Helping communities recognize risks early, prepare local response pathways, and keep essential health information moving during outbreaks.", priority_kicker="Program priority", priority_title="Practical action built around community needs.", points=["Community readiness sessions", "Early-warning communication", "Referral and response coordination"], image_url=image_url("images/im-04.jpeg"), image_alt="Volunteer supporting a household health activity"),
    "advocacy-and-health-promotions": item(slug="advocacy-and-health-promotions", title="Advocacy and Health Promotions", kicker="Focus area", summary="Supporting health education, public awareness, and trusted community conversations that help families act earlier and make informed choices.", priority_kicker="Program priority", priority_title="Practical action built around community needs.", points=["Health talks and campaigns", "Youth-centered awareness", "Community-led advocacy"], image_url=image_url("images/im-09.jpeg"), image_alt="Community members attending a Health Planet Foundation outreach session"),
    "wash": item(slug="wash", title="WASH", kicker="Focus area", summary="Promoting practical water, sanitation, and hygiene action so families can reduce preventable health risks in everyday life.", priority_kicker="Program priority", priority_title="Practical action built around community needs.", points=["Water safety demonstrations", "Hygiene promotion", "Household sanitation support"], image_url=image_url("images/im-15.jpeg"), image_alt="Program staff arranging WASH and community health supplies"),
}

FOCUS_AREA_LINKS = list(FOCUS_AREAS.values())

CAREER_OPENINGS = [
    item(role="Community Programs Coordinator", location="Lusaka, Zambia", employment_type="Full time"),
    item(role="Monitoring and Learning Assistant", location="Hybrid", employment_type="Contract"),
]

INTERNSHIPS = [
    item(role="Communications Intern", focus="Storytelling, campaigns, and partner updates", icon="IN"),
    item(role="Public Health Intern", focus="Field research, community sessions, and reporting support", icon="IN"),
]

DONATION_AMOUNTS = [
    item(amount="25", label="Field materials", select_value="25"),
    item(amount="50", label="Community session support", select_value="50"),
    item(amount="100", label="Training contribution", select_value="100"),
]
