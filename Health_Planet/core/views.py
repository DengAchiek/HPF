from django.http import Http404
from django.db.utils import OperationalError, ProgrammingError
from django.shortcuts import render

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


def get_page(slug):
    return safe_first(PageContent.objects.filter(slug=slug))


def get_sections(page_slug):
    sections = safe_list(SectionContent.objects.filter(page_slug=page_slug).order_by("key"))
    return {section.key: section for section in sections}


def base_page_context(slug):
    return {
        "page": get_page(slug),
        "sections": get_sections(slug),
    }


def home(request):
    context = base_page_context("home")
    context.update(
        {
            "features": safe_list(
                FeatureCard.objects.filter(
                    section_key="home_features",
                    is_active=True,
                )
            ),
            "stats": safe_list(StatItem.objects.filter(is_active=True)),
            "impact_points": safe_list(
                FeatureCard.objects.filter(
                    section_key="home_impact_points",
                    is_active=True,
                )
            ),
            "projects": safe_list(Project.objects.filter(is_active=True).order_by("sort_order", "id")),
            "news_items": safe_list(
                NewsItem.objects.filter(is_active=True).order_by("sort_order", "id")[:2]
            ),
            "gallery_images": safe_list(
                GalleryImage.objects.filter(
                    gallery_key="home_gallery",
                    is_active=True,
                ).order_by("sort_order", "id")
            ),
        }
    )
    return render(request, "home.html", context)


def about(request):
    context = base_page_context("about")
    context.update(
        {
            "about_slides": safe_list(
                GalleryImage.objects.filter(
                    gallery_key="about_slideshow",
                    is_active=True,
                ).order_by("sort_order", "id")
            ),
            "work_features": safe_list(
                FeatureCard.objects.filter(
                    section_key="about_work",
                    is_active=True,
                )
            ),
            "management_team": safe_list(
                TeamMember.objects.filter(
                    team=TeamMember.TEAM_MANAGEMENT,
                    is_active=True,
                )
            ),
            "board_members": safe_list(
                TeamMember.objects.filter(
                    team=TeamMember.TEAM_BOARD,
                    is_active=True,
                )
            ),
        }
    )
    return render(request, "about.html", context)


def projects(request):
    context = base_page_context("projects")
    context["projects"] = safe_list(Project.objects.filter(is_active=True).order_by("sort_order", "id"))
    return render(request, "projects.html", context)


def focus_area(request, slug):
    area = safe_first(FocusArea.objects.filter(slug=slug, is_active=True))
    if area is None:
        raise Http404("Focus area not found")

    context = base_page_context("focus_area")
    context["area"] = area
    return render(request, "focus_area.html", context)


def news(request):
    context = base_page_context("news")
    context["news_items"] = safe_list(
        NewsItem.objects.filter(is_active=True).order_by("sort_order", "id")
    )
    return render(request, "news.html", context)


def careers(request):
    context = base_page_context("careers")
    context["openings"] = safe_list(CareerOpening.objects.filter(is_active=True))
    return render(request, "careers.html", context)


def internships(request):
    context = base_page_context("internships")
    context["internships"] = safe_list(InternshipTrack.objects.filter(is_active=True))
    return render(request, "internships.html", context)


def donate(request):
    context = base_page_context("donate")
    context.update(
        {
            "amounts": safe_list(DonationAmount.objects.filter(is_active=True)),
            "submitted": request.method == "POST",
        }
    )
    return render(request, "donate.html", context)


def contact(request):
    context = base_page_context("contact")
    context["submitted"] = request.method == "POST"
    return render(request, "contact.html", context)
