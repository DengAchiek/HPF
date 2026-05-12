from django.http import Http404
from django.db.utils import OperationalError, ProgrammingError
from django.shortcuts import render

from . import defaults
from .models import (
    CareerOpening,
    DonationAmount,
    FeatureCard,
    FocusArea,
    GalleryImage,
    InternshipTrack,
    NewsItem,
    PageContent,
    Project,
    SectionContent,
    StatItem,
    TeamMember,
)


DB_ERRORS = (OperationalError, ProgrammingError)


def safe_first(queryset):
    try:
        return queryset.first()
    except DB_ERRORS:
        return None


def safe_list(queryset):
    try:
        return list(queryset)
    except DB_ERRORS:
        return []


def first_or_default(queryset, fallback):
    return safe_first(queryset) or fallback


def list_or_default(queryset, fallback):
    items = safe_list(queryset)
    return items or fallback


def get_page(slug):
    return first_or_default(
        PageContent.objects.filter(slug=slug),
        defaults.PAGES.get(slug),
    )


def get_sections(page_slug):
    default_sections = dict(defaults.SECTIONS.get(page_slug, {}))
    sections = safe_list(SectionContent.objects.filter(page_slug=page_slug).order_by("key"))
    default_sections.update({section.key: section for section in sections})
    return default_sections


def base_page_context(slug):
    return {
        "page": get_page(slug),
        "sections": get_sections(slug),
    }


def home(request):
    context = base_page_context("home")
    context.update(
        {
            "features": list_or_default(
                FeatureCard.objects.filter(
                    section_key="home_features",
                    is_active=True,
                ),
                defaults.FEATURES,
            ),
            "stats": list_or_default(
                StatItem.objects.filter(is_active=True),
                defaults.STATS,
            ),
            "impact_points": list_or_default(
                FeatureCard.objects.filter(
                    section_key="home_impact_points",
                    is_active=True,
                ),
                defaults.IMPACT_POINTS,
            ),
            "projects": list_or_default(
                Project.objects.filter(is_active=True).order_by("sort_order", "id"),
                defaults.PROJECTS,
            ),
            "news_items": list_or_default(
                NewsItem.objects.filter(is_active=True).order_by("sort_order", "id")[:2],
                defaults.NEWS_ITEMS[:2],
            ),
            "gallery_images": list_or_default(
                GalleryImage.objects.filter(
                    gallery_key="home_gallery",
                    is_active=True,
                ).order_by("sort_order", "id"),
                defaults.GALLERY_IMAGES,
            ),
            "partners": list_or_default(
                GalleryImage.objects.filter(
                    gallery_key="home_partners",
                    is_active=True,
                ).order_by("sort_order", "id"),
                defaults.PARTNERS,
            ),
        }
    )
    return render(request, "home.html", context)


def about(request):
    context = base_page_context("about")
    context.update(
        {
            "about_slides": list_or_default(
                GalleryImage.objects.filter(
                    gallery_key="about_slideshow",
                    is_active=True,
                ).order_by("sort_order", "id"),
                defaults.ABOUT_SLIDES,
            ),
            "work_features": list_or_default(
                FeatureCard.objects.filter(
                    section_key="about_work",
                    is_active=True,
                ),
                defaults.ABOUT_WORK_FEATURES,
            ),
            "management_team": list_or_default(
                TeamMember.objects.filter(
                    team=TeamMember.TEAM_MANAGEMENT,
                    is_active=True,
                ),
                defaults.MANAGEMENT_TEAM,
            ),
            "board_members": list_or_default(
                TeamMember.objects.filter(
                    team=TeamMember.TEAM_BOARD,
                    is_active=True,
                ),
                defaults.BOARD_MEMBERS,
            ),
        }
    )
    return render(request, "about.html", context)


def projects(request):
    context = base_page_context("projects")
    context["projects"] = list_or_default(
        Project.objects.filter(is_active=True).order_by("sort_order", "id"),
        defaults.PROJECTS,
    )
    return render(request, "projects.html", context)


def focus_area(request, slug):
    area = first_or_default(
        FocusArea.objects.filter(slug=slug, is_active=True),
        defaults.FOCUS_AREAS.get(slug),
    )
    if area is None:
        raise Http404("Focus area not found")

    context = base_page_context("focus_area")
    context["area"] = area
    return render(request, "focus_area.html", context)


def news(request):
    context = base_page_context("news")
    context["news_items"] = list_or_default(
        NewsItem.objects.filter(is_active=True).order_by("sort_order", "id"),
        defaults.NEWS_ITEMS,
    )
    return render(request, "news.html", context)


def careers(request):
    context = base_page_context("careers")
    context["openings"] = list_or_default(
        CareerOpening.objects.filter(is_active=True),
        defaults.CAREER_OPENINGS,
    )
    return render(request, "careers.html", context)


def internships(request):
    context = base_page_context("internships")
    context["internships"] = list_or_default(
        InternshipTrack.objects.filter(is_active=True),
        defaults.INTERNSHIPS,
    )
    return render(request, "internships.html", context)


def donate(request):
    context = base_page_context("donate")
    context.update(
        {
            "amounts": list_or_default(
                DonationAmount.objects.filter(is_active=True),
                defaults.DONATION_AMOUNTS,
            ),
            "submitted": request.method == "POST",
        }
    )
    return render(request, "donate.html", context)


def contact(request):
    context = base_page_context("contact")
    context["submitted"] = request.method == "POST"
    return render(request, "contact.html", context)
