from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db import connection
from django.db.utils import DatabaseError, OperationalError, ProgrammingError
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from careers.forms import ApplicationSubmissionForm
from careers.models import ApplicationSubmission
from contacts.forms import ContactSubmissionForm
from donations.forms import DonationInterestForm

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


def notify_team(subject, body, recipient):
    if not recipient:
        return
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=True,
    )


def seo_context(request, title, description, image_url=""):
    return {
        "seo_title": title,
        "seo_description": description,
        "seo_image": request.build_absolute_uri(image_url) if image_url else "",
        "canonical_url": request.build_absolute_uri(request.path),
    }


def base_page_context(slug, request=None):
    page = get_page(slug)
    context = {
        "page": page,
        "sections": get_sections(slug),
        "hero_slides": get_page_hero_slides(slug, page),
    }
    if request:
        context.update(
            seo_context(
                request,
                getattr(page, "meta_title", "") or getattr(page, "title", ""),
                getattr(page, "meta_description", "") or getattr(page, "hero_text", ""),
                getattr(page, "image_url", ""),
            )
        )
    return context


def home(request):
    context = base_page_context("home", request)
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
    context = base_page_context("about", request)
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
    context = base_page_context("projects", request)
    projects = list_or_default(
        Project.objects.filter(is_active=True).order_by("sort_order", "id"),
        defaults.PROJECTS,
    )
    context["projects"] = projects
    context["hero_slides"] = get_page_hero_slides("projects", context["page"], projects)
    return render(request, "projects.html", context)


def find_default_project(slug):
    for project in defaults.PROJECTS:
        if getattr(project, "slug", "") == slug:
            return project
    return None


def project_detail(request, slug):
    project = safe_first(
        Project.objects.prefetch_related("gallery_images").filter(slug=slug, is_active=True)
    )

    if project:
        gallery_images = safe_list(
            project.gallery_images.filter(is_active=True).order_by("sort_order", "id")
        )
        related_projects = safe_list(
            Project.objects.filter(is_active=True)
            .exclude(pk=project.pk)
            .order_by("sort_order", "id")[:3]
        )
    else:
        project = find_default_project(slug)
        if project is None:
            raise Http404("Project not found")
        gallery_images = getattr(project, "gallery_images", [])
        related_projects = [
            item for item in defaults.PROJECTS if getattr(item, "slug", "") != slug
        ][:3]

    context = base_page_context("projects", request)
    context.update(
        {
            "project": project,
            "gallery_images": gallery_images,
            "related_projects": related_projects,
            "hero_slides": build_hero_slides(
                getattr(project, "image_url", ""),
                getattr(project, "image_alt", ""),
                gallery_images,
            ),
        }
    )
    context.update(
        seo_context(
            request,
            f"{project.title} | Impact | Health Planet Foundation",
            project.description,
            getattr(project, "image_url", ""),
        )
    )
    return render(request, "project_detail.html", context)


def focus_area(request, slug):
    area = first_or_default(
        FocusArea.objects.filter(slug=slug, is_active=True),
        defaults.FOCUS_AREAS.get(slug),
    )
    if area is None:
        raise Http404("Focus area not found")

    context = base_page_context("focus_area", request)
    context["area"] = area
    context["hero_slides"] = get_hero_slides(
        f"focus_{slug}_hero",
        getattr(area, "image_url", ""),
        getattr(area, "image_alt", ""),
        defaults.FOCUS_HERO_SLIDES.get(slug, defaults.HERO_SLIDES.get("focus_area", [])),
    )
    context.update(
        seo_context(
            request,
            f"{area.title} | Health Planet Foundation",
            area.summary,
            getattr(area, "image_url", ""),
        )
    )
    return render(request, "focus_area.html", context)


def news(request):
    context = base_page_context("news", request)
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

    context = base_page_context("news", request)
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
    context.update(
        seo_context(
            request,
            f"{item.title} | News | Health Planet Foundation",
            item.summary,
            getattr(item, "image_url", ""),
        )
    )
    return render(request, "news_detail.html", context)


def careers(request):
    context = base_page_context("careers", request)
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
    context = base_page_context("internships", request)
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


def application_page(request, application_type):
    is_career = application_type == ApplicationSubmission.TYPE_CAREER
    page_slug = "careers" if is_career else "internships"
    redirect_name = "career_apply" if is_career else "internship_apply"
    context = base_page_context(page_slug, request)
    if is_career:
        opportunities = list_or_default(
            CareerOpening.objects.filter(is_active=True).order_by("sort_order", "id"),
            defaults.CAREER_OPENINGS,
        )
    else:
        opportunities = list_or_default(
            InternshipTrack.objects.filter(is_active=True).order_by("sort_order", "id"),
            defaults.INTERNSHIPS,
        )
    opportunity_labels = [opportunity.role for opportunity in opportunities]
    requested_opportunity = request.GET.get("opportunity", "")
    initial = (
        {"opportunity_label": requested_opportunity}
        if requested_opportunity in opportunity_labels
        else None
    )
    form = ApplicationSubmissionForm(
        request.POST or None,
        initial=initial,
        application_type=application_type,
        opportunities=opportunity_labels,
    )

    if request.method == "POST" and request.POST.get("website"):
        messages.success(request, "Thank you. Your application has been received.")
        return redirect(redirect_name)

    if request.method == "POST" and form.is_valid():
        submission = form.save()
        notify_team(
            "New website application received",
            (
                f"Type: {submission.get_application_type_display()}\n"
                f"Opportunity: {submission.opportunity_label}\n"
                f"Name: {submission.full_name}\n"
                f"Email: {submission.email}\n"
                f"Phone: {submission.phone or 'Not provided'}\n"
                f"Location: {submission.location or 'Not provided'}\n"
                f"CV or portfolio: {submission.cv_link or 'Not provided'}\n\n"
                f"Candidate message:\n{submission.cover_message}"
            ),
            settings.APPLICATION_NOTIFICATION_EMAIL,
        )
        messages.success(request, "Thank you. Your application has been received.")
        return redirect(redirect_name)

    context.update(
        {
            "application_form": form,
            "application_type": application_type,
            "application_title": "Career application" if is_career else "Internship application",
            "application_intro": (
                "Apply for a current role or submit a general career application."
                if is_career
                else "Tell us which internship track interests you and how you hope to contribute."
            ),
            "back_url_name": "careers" if is_career else "internships",
        }
    )
    context["hero_slides"] = get_page_hero_slides(page_slug, context["page"])
    context.update(
        seo_context(
            request,
            f"{context['application_title']} | Health Planet Foundation",
            context["application_intro"],
            getattr(context["page"], "image_url", ""),
        )
    )
    return render(request, "application.html", context)


def career_apply(request):
    return application_page(request, ApplicationSubmission.TYPE_CAREER)


def internship_apply(request):
    return application_page(request, ApplicationSubmission.TYPE_INTERNSHIP)


def donate(request):
    context = base_page_context("donate", request)
    hero_sources = [
        context["sections"].get("donate_details"),
        *defaults.HERO_SLIDES.get("donate", []),
    ]
    amounts = list_or_default(
        DonationAmount.objects.filter(is_active=True),
        defaults.DONATION_AMOUNTS,
    )
    form = DonationInterestForm(request.POST or None, amounts=amounts)

    if request.method == "POST" and request.POST.get("website"):
        messages.success(
            request,
            "Thank you. Your support interest has been received and our team will follow up.",
        )
        return redirect("donate")

    if request.method == "POST" and form.is_valid():
        submission = form.save()
        notify_team(
            "New donation interest submitted through the website",
            (
                f"Name: {submission.full_name}\n"
                f"Email: {submission.email}\n"
                f"Phone: {submission.phone or 'Not provided'}\n"
                f"Preferred amount: {submission.display_amount}\n\n"
                f"Note:\n{submission.message or 'No note provided.'}"
            ),
            settings.DONATION_NOTIFICATION_EMAIL,
        )
        messages.success(
            request,
            "Thank you. Your support interest has been received and our team will follow up.",
        )
        return redirect("donate")

    context.update(
        {
            "amounts": amounts,
            "form": form,
        }
    )
    context["hero_slides"] = get_page_hero_slides("donate", context["page"], hero_sources)
    return render(request, "donate.html", context)


def contact(request):
    context = base_page_context("contact", request)
    form = ContactSubmissionForm(request.POST or None)

    if request.method == "POST" and request.POST.get("website"):
        messages.success(request, "Thank you. Your message has been received.")
        return redirect("contact")

    if request.method == "POST" and form.is_valid():
        submission = form.save()
        notify_team(
            "New website contact enquiry",
            (
                f"Name: {submission.full_name}\n"
                f"Email: {submission.email}\n"
                f"Phone: {submission.phone or 'Not provided'}\n"
                f"Organization: {submission.organization or 'Not provided'}\n\n"
                f"Message:\n{submission.message}"
            ),
            settings.CONTACT_NOTIFICATION_EMAIL,
        )
        messages.success(request, "Thank you. Your message has been received.")
        return redirect("contact")

    context["form"] = form
    context["hero_slides"] = get_page_hero_slides(
        "contact",
        context["page"],
        [
            context["sections"].get("contact_details"),
            *defaults.HERO_SLIDES.get("contact", []),
        ],
    )
    return render(request, "contact.html", context)


def privacy(request):
    return render(request, "privacy.html", base_page_context("privacy", request))


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    content = f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {sitemap_url}\n"
    return HttpResponse(content, content_type="text/plain")


def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError:
        return JsonResponse({"status": "unavailable", "database": "error"}, status=503)
    return JsonResponse({"status": "ok", "database": "ok"})
