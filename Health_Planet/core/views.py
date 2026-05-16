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


def build_hero_slides(primary_image="", primary_alt="", slides=None):
    hero_slides = []
    seen_urls = set()

    def add_slide(image_url, image_alt="", caption=""):
        if not image_url or image_url in seen_urls:
            return
        seen_urls.add(image_url)
        hero_slides.append(
            defaults.item(
                image_url=image_url,
                image_alt=image_alt,
                caption=caption,
            )
        )

    add_slide(primary_image, primary_alt)
    for slide in slides or []:
        add_slide(
            getattr(slide, "image_url", ""),
            getattr(slide, "image_alt", ""),
            getattr(slide, "caption", ""),
        )

    if not hero_slides:
        add_slide(defaults.image_url("images/im-01.jpeg"), "Health Planet Foundation field work")

    while len(hero_slides) < 6:
        hero_slides.extend(hero_slides[: 6 - len(hero_slides)])

    return hero_slides[:6]


def get_hero_slides(gallery_key, primary_image="", primary_alt="", fallback_slides=None):
    admin_slides = safe_list(
        GalleryImage.objects.filter(
            gallery_key=gallery_key,
            is_active=True,
        ).order_by("sort_order", "id")
    )
    slides = admin_slides or fallback_slides or []
    return build_hero_slides(primary_image, primary_alt, slides)


def get_page_hero_slides(page_slug, page, fallback_slides=None):
    return get_hero_slides(
        f"{page_slug}_hero",
        getattr(page, "image_url", ""),
        getattr(page, "image_alt", ""),
        fallback_slides or defaults.HERO_SLIDES.get(page_slug, []),
    )


def base_page_context(slug):
    page = get_page(slug)
    return {
        "page": page,
        "sections": get_sections(slug),
        "hero_slides": get_page_hero_slides(slug, page),
    }


def home(request):
    context = base_page_context("home")
    gallery_images = list_or_default(
        GalleryImage.objects.filter(
            gallery_key="home_gallery",
            is_active=True,
        ).order_by("sort_order", "id"),
        defaults.GALLERY_IMAGES,
    )
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
            "gallery_images": gallery_images,
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
    about_slides = list_or_default(
        GalleryImage.objects.filter(
            gallery_key="about_slideshow",
            is_active=True,
        ).order_by("sort_order", "id"),
        defaults.ABOUT_SLIDES,
    )
    context.update(
        {
            "about_slides": about_slides,
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
    context["hero_slides"] = get_page_hero_slides("about", context["page"], about_slides)
    return render(request, "about.html", context)


def projects(request):
    context = base_page_context("projects")
    projects = list_or_default(
        Project.objects.filter(is_active=True).order_by("sort_order", "id"),
        defaults.PROJECTS,
    )
    context["projects"] = projects
    context["hero_slides"] = get_page_hero_slides("projects", context["page"], projects)
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
    context["hero_slides"] = get_hero_slides(
        f"focus_{slug}_hero",
        getattr(area, "image_url", ""),
        getattr(area, "image_alt", ""),
        defaults.FOCUS_HERO_SLIDES.get(slug, defaults.HERO_SLIDES.get("focus_area", [])),
    )
    return render(request, "focus_area.html", context)


def news(request):
    context = base_page_context("news")
    news_items = list_or_default(
        NewsItem.objects.filter(is_active=True).order_by("sort_order", "id"),
        defaults.NEWS_ITEMS,
    )
    context["news_items"] = news_items
    context["hero_slides"] = get_page_hero_slides("news", context["page"], news_items)
    return render(request, "news.html", context)


def find_default_news_item(slug):
    for item in defaults.NEWS_ITEMS:
        if getattr(item, "slug", "") == slug:
            return item
    return None


def news_detail(request, slug):
    item = safe_first(
        NewsItem.objects.prefetch_related("gallery_images").filter(slug=slug, is_active=True)
    )

    if item:
        gallery_images = safe_list(
            item.gallery_images.filter(is_active=True).order_by("sort_order", "id")
        )
        related_news = safe_list(
            NewsItem.objects.filter(is_active=True)
            .exclude(pk=item.pk)
            .order_by("sort_order", "id")[:3]
        )
        article_body = item.article_body
    else:
        item = find_default_news_item(slug)
        if item is None:
            raise Http404("News item not found")
        gallery_images = getattr(item, "gallery_images", [])
        related_news = [
            related_item
            for related_item in defaults.NEWS_ITEMS
            if getattr(related_item, "slug", "") != slug
        ][:3]
        article_body = getattr(item, "body", "") or item.summary

    context = base_page_context("news")
    context.update(
        {
            "item": item,
            "article_body": article_body,
            "gallery_images": gallery_images,
            "related_news": related_news,
            "hero_slides": build_hero_slides(
                getattr(item, "image_url", ""),
                getattr(item, "image_alt", ""),
                gallery_images,
            ),
        }
    )
    return render(request, "news_detail.html", context)


def careers(request):
    context = base_page_context("careers")
    hero_sources = [
        context["sections"].get("careers_intro"),
        *defaults.HERO_SLIDES.get("careers", []),
    ]
    context["openings"] = list_or_default(
        CareerOpening.objects.filter(is_active=True),
        defaults.CAREER_OPENINGS,
    )
    context["hero_slides"] = get_page_hero_slides("careers", context["page"], hero_sources)
    return render(request, "careers.html", context)


def internships(request):
    context = base_page_context("internships")
    hero_sources = [
        context["sections"].get("internships_intro"),
        *defaults.HERO_SLIDES.get("internships", []),
    ]
    context["internships"] = list_or_default(
        InternshipTrack.objects.filter(is_active=True),
        defaults.INTERNSHIPS,
    )
    context["hero_slides"] = get_page_hero_slides("internships", context["page"], hero_sources)
    return render(request, "internships.html", context)


def donate(request):
    context = base_page_context("donate")
    hero_sources = [
        context["sections"].get("donate_details"),
        *defaults.HERO_SLIDES.get("donate", []),
    ]
    context.update(
        {
            "amounts": list_or_default(
                DonationAmount.objects.filter(is_active=True),
                defaults.DONATION_AMOUNTS,
            ),
            "submitted": request.method == "POST",
        }
    )
    context["hero_slides"] = get_page_hero_slides("donate", context["page"], hero_sources)
    return render(request, "donate.html", context)


def contact(request):
    context = base_page_context("contact")
    context["submitted"] = request.method == "POST"
    context["hero_slides"] = get_page_hero_slides(
        "contact",
        context["page"],
        [
            context["sections"].get("contact_details"),
            *defaults.HERO_SLIDES.get("contact", []),
        ],
    )
    return render(request, "contact.html", context)
