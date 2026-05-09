from django.shortcuts import render


PROJECTS = [
    {
        "title": "Climate-Smart Clinics",
        "description": "Helping rural health posts prepare for heat, flooding, and service disruption through local planning and practical resilience tools.",
        "status": "Active",
        "image": "images/im-13.jpeg",
        "image_alt": "Health Planet Foundation team members preparing field materials",
    },
    {
        "title": "Safe Motherhood Circles",
        "description": "Community-led sessions connecting expectant mothers with health information, referral support, and trusted peer networks.",
        "status": "Field program",
        "image": "images/im-17.jpeg",
        "image_alt": "Community session with mothers and health volunteers",
    },
    {
        "title": "Youth Mental Wellness",
        "description": "School and community outreach that makes mental health conversations easier, earlier, and connected to local care pathways.",
        "status": "Growing",
        "image": "images/im-19.jpeg",
        "image_alt": "Young people and community leaders gathering outdoors",
    },
]

NEWS_ITEMS = [
    {
        "title": "Community health volunteers expand outreach in Lusaka Province",
        "date": "May 2026",
        "summary": "New volunteer cohorts are supporting health talks, referrals, and preparedness conversations in high-risk communities.",
        "image": "images/im-09.jpeg",
        "image_alt": "Community members attending a Health Planet Foundation outreach session",
    },
    {
        "title": "Climate resilience sessions reach district health teams",
        "date": "April 2026",
        "summary": "District teams reviewed practical response plans for heat stress, water safety, and continuity of essential services.",
        "image": "images/im-08.jpeg",
        "image_alt": "Field preparation work at a community site",
    },
    {
        "title": "Youth wellness clubs launch a peer-support calendar",
        "date": "March 2026",
        "summary": "Young leaders are creating consistent spaces for mental wellness education and early help-seeking.",
        "image": "images/im-01.jpeg",
        "image_alt": "Youth and community members seated during an outdoor session",
    },
]

CAREER_OPENINGS = [
    {
        "role": "Community Programs Coordinator",
        "location": "Lusaka, Zambia",
        "type": "Full time",
    },
    {
        "role": "Monitoring and Learning Assistant",
        "location": "Hybrid",
        "type": "Contract",
    },
]

INTERNSHIPS = [
    {
        "role": "Communications Intern",
        "focus": "Storytelling, campaigns, and partner updates",
    },
    {
        "role": "Public Health Intern",
        "focus": "Field research, community sessions, and reporting support",
    },
]

GALLERY_IMAGES = [
    {
        "src": "images/im-01.jpeg",
        "alt": "Community members gathered outdoors for a Health Planet Foundation session",
        "caption": "Outdoor health talk",
        "focus": "focus-center",
    },
    {
        "src": "images/im-02.jpeg",
        "alt": "Community group gathered for a health discussion",
        "caption": "Community dialogue",
        "focus": "focus-center",
    },
    {
        "src": "images/im-03.jpeg",
        "alt": "Health Planet Foundation volunteers speaking with community members",
        "caption": "Field outreach",
        "focus": "focus-upper",
    },
    {
        "src": "images/im-04.jpeg",
        "alt": "Volunteer supporting a household health activity",
        "caption": "Household support",
        "focus": "focus-upper",
    },
    {
        "src": "images/im-05.jpeg",
        "alt": "Team member demonstrating handwashing and water safety materials",
        "caption": "Practical demos",
        "focus": "focus-upper",
    },
    {
        "src": "images/im-06.jpeg",
        "alt": "Children and adults gathered under a tree for community programming",
        "caption": "Local participation",
        "focus": "focus-upper",
    },
    {
        "src": "images/im-07.jpeg",
        "alt": "Community members receiving support during an outdoor session",
        "caption": "Trusted presence",
        "focus": "focus-upper",
    },
    {
        "src": "images/im-08.jpeg",
        "alt": "Field preparation work at a community site",
        "caption": "Site preparation",
        "focus": "focus-center",
    },
    {
        "src": "images/im-09.jpeg",
        "alt": "Community members waiting during a Health Planet Foundation outreach day",
        "caption": "Outreach day",
        "focus": "focus-center",
    },
    {
        "src": "images/im-10.jpeg",
        "alt": "Health Planet Foundation staff member speaking with a mother during a home visit",
        "caption": "Home visit",
        "focus": "focus-upper",
    },
    {
        "src": "images/im-11.jpeg",
        "alt": "Team member holding program supplies for community outreach",
        "caption": "Program supplies",
        "focus": "focus-center",
    },
    {
        "src": "images/im-12.jpeg",
        "alt": "Health Planet Foundation team member supporting a community health activity",
        "caption": "Hands-on support",
        "focus": "focus-center",
    },
    {
        "src": "images/im-13.jpeg",
        "alt": "Health Planet Foundation team with field materials",
        "caption": "Prepared teams",
        "focus": "focus-center",
    },
    {
        "src": "images/im-14.jpeg",
        "alt": "Health Planet Foundation team with field supplies",
        "caption": "Field supplies",
        "focus": "focus-center",
    },
    {
        "src": "images/im-15.jpeg",
        "alt": "Program staff arranging community health supplies",
        "caption": "Field materials",
        "focus": "focus-center",
    },
    {
        "src": "images/im-16.jpeg",
        "alt": "Intern supporting a community health activity",
        "caption": "Learning through service",
        "focus": "focus-upper",
    },
    {
        "src": "images/im-17.jpeg",
        "alt": "Community session with mothers and health volunteers",
        "caption": "Motherhood circle",
        "focus": "focus-center",
    },
    {
        "src": "images/im-18.jpeg",
        "alt": "Health Planet Foundation team speaking with community members",
        "caption": "Community meeting",
        "focus": "focus-center",
    },
    {
        "src": "images/im-19.jpeg",
        "alt": "Young people and community leaders gathering outdoors",
        "caption": "Youth engagement",
        "focus": "focus-upper",
    },
    {
        "src": "images/im-20.jpeg",
        "alt": "Health Planet Foundation volunteer supporting bedside care",
        "caption": "Care support",
        "focus": "focus-upper",
    },
]


def home(request):
    context = {
        "projects": PROJECTS,
        "news_items": NEWS_ITEMS[:2],
        "gallery_images": GALLERY_IMAGES,
    }
    return render(request, "home.html", context)


def about(request):
    return render(request, "about.html")


def projects(request):
    return render(request, "projects.html", {"projects": PROJECTS})


def news(request):
    return render(request, "news.html", {"news_items": NEWS_ITEMS})


def careers(request):
    return render(request, "careers.html", {"openings": CAREER_OPENINGS})


def internships(request):
    return render(request, "internships.html", {"internships": INTERNSHIPS})


def donate(request):
    context = {"submitted": request.method == "POST"}
    return render(request, "donate.html", context)


def contact(request):
    context = {"submitted": request.method == "POST"}
    return render(request, "contact.html", context)
