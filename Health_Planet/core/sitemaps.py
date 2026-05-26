from django.contrib.sitemaps import Sitemap
from django.db.utils import OperationalError, ProgrammingError
from django.urls import reverse

from . import defaults
from .models import FocusArea, NewsItem, Project


def list_or_default(queryset, fallback):
    try:
        items = list(queryset)
    except (OperationalError, ProgrammingError):
        items = []
    return items or fallback


class StaticPageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return ("home", "about", "projects", "news", "careers", "internships", "donate", "contact", "privacy")

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return list_or_default(
            Project.objects.filter(is_active=True).order_by("sort_order", "id"),
            defaults.PROJECTS,
        )

    def location(self, item):
        return item.detail_href


class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return list_or_default(
            NewsItem.objects.filter(is_active=True).order_by("sort_order", "id"),
            defaults.NEWS_ITEMS,
        )

    def location(self, item):
        return item.detail_href


class FocusAreaSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return list_or_default(
            FocusArea.objects.filter(is_active=True).order_by("sort_order", "id"),
            defaults.FOCUS_AREA_LINKS,
        )

    def location(self, item):
        return reverse("focus_area", kwargs={"slug": item.slug})


sitemaps = {
    "pages": StaticPageSitemap,
    "projects": ProjectSitemap,
    "news": NewsSitemap,
    "focus_areas": FocusAreaSitemap,
}
