from datetime import date
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


def gallery_image(static_image, image_alt="", caption="", sort_order=0):
    return item(
        static_image=static_image,
        image_alt=image_alt,
        caption=caption,
        sort_order=sort_order,
        image_url=image_url(static_image),
    )


def news_item(
    slug,
    title,
    date_label,
    summary,
    static_image,
    image_alt,
    event_date=None,
    venue="",
    participants="",
    body="",
    gallery_images=None,
):
    return item(
        slug=slug,
        title=title,
        date_label=date_label,
        event_date=event_date,
        venue=venue,
        participants=participants,
        summary=summary,
        body=body or summary,
        static_image=static_image,
        image_alt=image_alt,
        image_url=image_url(static_image),
        detail_href=f"/news/{slug}/",
        gallery_images=gallery_images or [
            gallery_image(static_image, image_alt, title, 10),
        ],
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

HERO_SLIDES = {
    "home": [
        gallery_image("images/im-01.jpeg", "Community members gathered outdoors for a Health Planet Foundation session", "Outdoor health talk"),
        gallery_image("images/im-02.jpeg", "Community group gathered for a health discussion", "Community dialogue"),
        gallery_image("images/im-03.jpeg", "Health Planet Foundation volunteers speaking with community members", "Field outreach"),
        gallery_image("images/im-06.jpeg", "Children and adults gathered under a tree for community programming", "Local participation"),
        gallery_image("images/im-07.jpeg", "Community members receiving support during an outdoor session", "Trusted presence"),
        gallery_image("images/im-12.jpeg", "Health Planet Foundation team member supporting a community health activity", "Hands-on support"),
    ],
    "about": [
        gallery_image("images/im-09.jpeg", "Community members attending a Health Planet Foundation outreach session", "Outreach day"),
        gallery_image("images/im-10.jpeg", "Health Planet Foundation staff member speaking with a mother during a home visit", "Home visit"),
        gallery_image("images/im-11.jpeg", "Team member holding program supplies for community outreach", "Program supplies"),
        gallery_image("images/im-20.jpeg", "Health Planet Foundation volunteer supporting bedside care", "Care support"),
    ],
    "projects": [
        gallery_image("images/im-13.jpeg", "Health Planet Foundation team with field materials", "Prepared teams"),
        gallery_image("images/im-14.jpeg", "Health Planet Foundation team with field supplies", "Field supplies"),
        gallery_image("images/im-15.jpeg", "Program staff arranging community health supplies", "Field materials"),
        gallery_image("images/im-17.jpeg", "Community session with mothers and health volunteers", "Motherhood circle"),
    ],
    "focus_area": [
        gallery_image("images/im-04.jpeg", "Volunteer supporting a household health activity", "Household support"),
        gallery_image("images/im-05.jpeg", "Team member demonstrating handwashing and water safety materials", "Practical demos"),
        gallery_image("images/im-09.jpeg", "Community members attending a Health Planet Foundation outreach session", "Outreach day"),
        gallery_image("images/im-15.jpeg", "Program staff arranging WASH and community health supplies", "Field materials"),
    ],
    "news": [
        gallery_image("images/news/rana-bootcamp-2026.jpg", "Plenary session at the RANA Bootcamp in Nairobi", "RANA Bootcamp"),
        gallery_image("images/news/rana-bootcamp-2026-group.jpg", "Participants at the RANA Bootcamp in Nairobi", "Regional partners"),
        gallery_image("images/news/continental-conference-lusaka-2026.jpg", "Delegates at the continental conference plenary session in Lusaka", "Continental conference"),
        gallery_image("images/news/continental-conference-lusaka-2026-panel.jpg", "Panel discussion at the continental conference in Lusaka", "Panel dialogue"),
    ],
    "careers": [
        gallery_image("images/im-19.jpeg", "Young people and community leaders gathering outdoors", "Youth engagement"),
        gallery_image("images/im-13.jpeg", "Health Planet Foundation team with field materials", "Prepared teams"),
        gallery_image("images/im-11.jpeg", "Team member holding program supplies for community outreach", "Program supplies"),
    ],
    "internships": [
        gallery_image("images/im-16.jpeg", "Intern supporting a community health activity", "Learning through service"),
        gallery_image("images/im-06.jpeg", "Children and adults gathered under a tree for community programming", "Local participation"),
        gallery_image("images/im-19.jpeg", "Young people and community leaders gathering outdoors", "Youth engagement"),
    ],
    "donate": [
        gallery_image("images/im-15.jpeg", "Program staff arranging community health supplies", "Field materials"),
        gallery_image("images/im-14.jpeg", "Health Planet Foundation team with field supplies", "Field supplies"),
        gallery_image("images/im-20.jpeg", "Health Planet Foundation volunteer supporting bedside care", "Care support"),
    ],
    "contact": [
        gallery_image("images/im-18.jpeg", "Health Planet Foundation team speaking with community members", "Community meeting"),
        gallery_image("images/im-10.jpeg", "Health Planet Foundation staff member speaking with a mother during a home visit", "Home visit"),
        gallery_image("images/im-09.jpeg", "Community members attending a Health Planet Foundation outreach session", "Outreach day"),
    ],
}

FOCUS_HERO_SLIDES = {
    "epidemic-preparedness": [
        gallery_image("images/im-04.jpeg", "Volunteer supporting a household health activity", "Household support"),
        gallery_image("images/im-08.jpeg", "Field preparation work at a community site", "Site preparation"),
        gallery_image("images/im-18.jpeg", "Health Planet Foundation team speaking with community members", "Community meeting"),
    ],
    "advocacy-and-health-promotions": [
        gallery_image("images/im-09.jpeg", "Community members attending a Health Planet Foundation outreach session", "Outreach day"),
        gallery_image("images/im-03.jpeg", "Health Planet Foundation volunteers speaking with community members", "Field outreach"),
        gallery_image("images/im-19.jpeg", "Young people and community leaders gathering outdoors", "Youth engagement"),
    ],
    "wash": [
        gallery_image("images/im-15.jpeg", "Program staff arranging WASH and community health supplies", "Field materials"),
        gallery_image("images/im-05.jpeg", "Team member demonstrating handwashing and water safety materials", "Practical demos"),
        gallery_image("images/im-07.jpeg", "Community members receiving support during an outdoor session", "Trusted presence"),
    ],
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
        "home_partners",
        kicker="Partners",
        title="Our partners",
        body="Health Planet Foundation works alongside public institutions and implementing partners to strengthen community health, resilience, and public service delivery.",
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
    item(
        icon="01",
        title="CLIMATE RESILIENCE & AGRICULTURE",
        body='Training communities in climate-smart agriculture and agroforestry to boost food security.\n\nTree Planting & Reforestation: Engaging in community-driven afforestation to restore landscapes, improve biodiversity, and prevent soil erosion.\n\nWaste Segregation & Management: Implementing "waste-to-wealth" projects in peri-urban areas to convert solid waste into compost and recyclable products.',
    ),
    item(
        icon="02",
        title="WASH",
        body="(Water, Sanitation, and Hygiene): Improving access to safe water and sanitation to build resilience against extreme weather.",
    ),
    item(
        icon="03",
        title="MENTAL HEALTH MANAGEMENT",
        body="Integrating mental health support for communities affected by climate disasters, droughts, and poverty.",
    ),
    item(
        icon="04",
        title="SAFE MOTHERHOOD",
        body="Family Planning & Health: Promoting sustainable population growth and reproductive health services in communities.",
    ),
    item(
        icon="05",
        title="SRH AWARENESS",
        body="Raising awareness on sexual and reproductive health rights, family planning, and gender-based violence prevention.",
    ),
    item(
        icon="06",
        title="EPIDEMIC PREPAREDNESS",
        body="Strengthening community readiness and response to disease outbreaks through training and early warning systems.",
    ),
    item(
        icon="07",
        title="ADVOCACY & HEALTH PROMOTIONS",
        body="Advocating for community health rights and promoting healthy behaviours through campaigns, media, and grassroots engagement.",
    ),
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
    news_item(
        slug="rana-bootcamp-advances-epidemic-preparedness-across-africa",
        title="RANA Bootcamp advances epidemic preparedness across Africa",
        date_label="28-30 April 2026",
        event_date=date(2026, 4, 28),
        venue="The Tribe Hotel, Nairobi, Kenya",
        participants="Civil society and community organizations from 11 African countries",
        summary="The Resilience Action Network Africa (RANA), in partnership with Resolve to Save Lives, convened civil society and community organizations from 11 African countries to establish a shared agenda for epidemic preparedness and community-engaged disease surveillance. HFPZ was represented by Executive Director Doreen McGeachy.",
        body="The Resilience Action Network Africa (RANA), in partnership with Resolve to Save Lives, convened civil society and community organizations from 11 African countries for a focused bootcamp on epidemic preparedness and community-engaged disease surveillance.\n\nHeld at The Tribe Hotel in Nairobi, Kenya from 28 to 30 April 2026, the bootcamp created space for organizations to align on a shared agenda for stronger disease surveillance ecosystems across Africa.\n\nThe discussions took place alongside the World Health Summit Regional Meeting and contributed to the Declaration for an Enabling Disease Surveillance Ecosystem, emphasizing collaboration, readiness, and community trust.\n\nHealth Planet Foundation Zambia was represented by Executive Director Doreen McGeachy, who contributed to the continental dialogue on practical approaches for preparedness and response.",
        static_image="images/news/rana-bootcamp-2026.jpg",
        image_alt="Plenary session at the RANA Bootcamp in Nairobi",
        gallery_images=[
            gallery_image(
                "images/news/rana-bootcamp-2026.jpg",
                "Plenary session at the RANA Bootcamp in Nairobi",
                "RANA Bootcamp plenary session",
                10,
            ),
            gallery_image(
                "images/news/rana-bootcamp-2026-group.jpg",
                "Participants at the RANA Bootcamp in Nairobi",
                "Regional partners gathered in Nairobi",
                20,
            ),
        ],
    ),
    news_item(
        slug="hpfz-joins-continental-dialogue-on-demographic-dividend-and-reproductive-health",
        title="HFPZ joins continental dialogue on demographic dividend and reproductive health",
        date_label="8-10 April 2026",
        event_date=date(2026, 4, 8),
        venue="Intercontinental Hotel, Lusaka, Zambia",
        participants="Over 200 delegates from across Africa",
        summary="The 1st Continental Conference for Non-State Actors on the Demographic Dividend and Reproductive Health brought together civil society, academia, private sector leaders, and youth advocates. HFPZ Programs Manager Nolia Chipundo participated in the dialogue supporting the Lusaka 2026 Call for Action.",
        body="The 1st Continental Conference for Non-State Actors on the Demographic Dividend and Reproductive Health was held from 8 to 10 April 2026 at the Intercontinental Hotel in Lusaka, Zambia.\n\nThe conference brought together more than 200 delegates from across Africa, including civil society organizations, academia, private sector leaders, and youth advocates.\n\nConvening partners included AUDA-NEPAD, Med Rap Zambia, UNAIDS, and the University of Zambia. The key outcome was the Lusaka 2026 Call for Action, which strengthened the role of non-state actors in advancing demographic dividend and reproductive health priorities.\n\nHealth Planet Foundation Zambia was represented by Programs Manager Nolia Chipundo. The event closed with a 5km solidarity walk from Pamodzi Hotel to the University of Zambia.",
        static_image="images/news/continental-conference-lusaka-2026.jpg",
        image_alt="Delegates at the continental conference plenary session in Lusaka",
        gallery_images=[
            gallery_image(
                "images/news/continental-conference-lusaka-2026.jpg",
                "Delegates at the continental conference plenary session in Lusaka",
                "Conference plenary session",
                10,
            ),
            gallery_image(
                "images/news/continental-conference-lusaka-2026-panel.jpg",
                "Panel discussion at the continental conference in Lusaka",
                "Panel dialogue",
                20,
            ),
            gallery_image(
                "images/news/continental-conference-lusaka-2026-delegates.jpg",
                "Delegates participating in the continental conference",
                "Delegates in session",
                30,
            ),
            gallery_image(
                "images/news/continental-conference-lusaka-2026-walk.jpg",
                "Solidarity walk during the continental conference",
                "Solidarity walk",
                40,
            ),
        ],
    ),
    news_item(
        slug="community-health-volunteers-expand-outreach-in-lusaka-province",
        title="Community health volunteers expand outreach in Lusaka Province",
        date_label="May 2026",
        summary="New volunteer cohorts are supporting health talks, referrals, and preparedness conversations in high-risk communities.",
        static_image="images/im-09.jpeg",
        image_alt="Community members attending a Health Planet Foundation outreach session",
    ),
    news_item(
        slug="climate-resilience-sessions-reach-district-health-teams",
        title="Climate resilience sessions reach district health teams",
        date_label="April 2026",
        summary="District teams reviewed practical response plans for heat stress, water safety, and continuity of essential services.",
        static_image="images/im-08.jpeg",
        image_alt="Field preparation work at a community site",
    ),
    news_item(
        slug="youth-wellness-clubs-launch-a-peer-support-calendar",
        title="Youth wellness clubs launch a peer-support calendar",
        date_label="March 2026",
        summary="Young leaders are creating consistent spaces for mental wellness education and early help-seeking.",
        static_image="images/im-01.jpeg",
        image_alt="Youth and community members seated during an outdoor session",
    ),
]

PARTNERS = [
    item(
        image_url=image_url("images/partners/ministry-health.svg"),
        image_alt="Ministry of Health logo",
        caption="Ministry of Health",
        focus_class="partner-wide",
    ),
    item(
        image_url=image_url("images/partners/rana.svg"),
        image_alt="RANA logo",
        caption="RANA",
        focus_class="partner-wide",
    ),
    item(
        image_url=image_url("images/partners/resolve-to-save-lives.svg"),
        image_alt="Resolve to Save Lives logo",
        caption="Resolve to Save Lives",
        focus_class="partner-wide",
    ),
    item(
        image_url=image_url("images/partners/thrive-aid.svg"),
        image_alt="Thrive Aid logo",
        caption="Thrive Aid",
        focus_class="partner-square",
    ),
    item(
        image_url=image_url("images/partners/ministry-community-development-social-services.svg"),
        image_alt="Ministry of Community Development and Social Services logo",
        caption="Ministry of Community Development and Social Services",
        focus_class="partner-wide",
    ),
    item(
        image_url=image_url("images/partners/ministry-green-economy-environment.svg"),
        image_alt="Ministry of Green Economy and Environment logo",
        caption="Ministry of Green Economy and Environment",
        focus_class="partner-wide",
    ),
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
    team_member("management", "Doreen McGeachy", "Executive Director", "Masters candidate for Public Health; degree in Public Health. Over 15 years of experience in the NGO and Health sectors with expertise in project programming and implementation.", "images/staff/doreen-mcgeachy.jpg"),
    team_member("management", "Maureen Nyambe", "Technical Advisor", "Holds a Masters degree in Public Health. Over 20 years of experience in the NGO and Health sectors with significant expertise in technical advising, project programming and implementation.", "images/staff/maureen-nyambe.jpg"),
    team_member("management", "Nolia Chipundo", "Programs Manager", "Holds an MSc in Project Management and CA Zambia qualification. Brings over 5 years of project management experience and over 10 years of financial expertise across the non-profit, private, and government sectors.", "images/staff/nolia-chipundo.jpg"),
    team_member("management", "Mercy Chipundo", "Finance & Administration Manager", "An accountant with over 10 years of experience managing organizational budgets and workplans. Holds a Diploma in Accountancy.", "images/staff/mercy-chipundo.jpg"),
]

BOARD_MEMBERS = [
    team_member("board", "Liyoka Liyoka", "Chairperson", "A dedicated development practitioner with over 15 years of experience in community health, youth empowerment, and climate resilience. Known for strong leadership and collaborative skills.", "images/staff/liyoka-liyoka.jpg"),
    team_member("board", "Yapoma Nkhoma", "Board Secretary", "A seasoned professional with over 25 years of experience in pharmacy, public health logistics, and supply chain management. Holds DipPharm, BPharm, MSc in Procurement & Logistics, and LLB.", "images/staff/yapoma-nkhoma.jpg"),
    team_member("board", "Bupe Harriet Mutale", "Director Finance", "Holds qualifications in Economics (BA) and Accounting (ACCA). Over 7 to 10 years of experience in insurance, auditing, and corporate advisory roles.", "images/staff/bupe-harriet-mutale-portrait.jpg"),
    team_member("board", "Tawanda Nyandoro", "Director Human Resources", "A seasoned Human Resource and Administration professional with 10 years of progressive experience across FMCG, Logistics, NGO and Banking sectors. Holds a Masters Degree in Human Resource Management from the National Institute of Public Administration (NIPA) and several other professional certifications.", "images/staff/tawanda-nyandoro.jpg"),
    team_member("board", "Dr. Gladys Muyembe", "Director Programs", "A dental and public health specialist with more than 15 years of professional experience. Holds expertise in public health programming and serves as Vice President of the Zambia Dental Association (ZDA).", "images/staff/gladys-muyembe.jpg"),
    team_member("board", "Salome Sichali", "Director Advocacy & Health Promotions", "A senior development professional with over 20 years of experience in governance, gender integration, civil society strengthening, and strategic partnerships. Holds a BA in Development Studies.", "images/staff/salome-sichali.jpg"),
    team_member("board", "Lujenda Kholoma", "Director Monitoring & Evaluation", "An M&E and public health professional with over a decade of experience. Holds an MPH in Population Studies & Global Health, Postgraduate Diploma in M&E, and BA in Demography and Development Studies.", "images/staff/lujenda-kholoma-portrait.jpg"),
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
