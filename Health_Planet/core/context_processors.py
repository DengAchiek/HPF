from django.db.utils import OperationalError, ProgrammingError

from . import defaults
from .models import FocusArea, FooterLink, NavigationItem, SiteSettings


FOOTER_GROUPS = (
    FooterLink.GROUP_PROGRAMS,
    FooterLink.GROUP_ORGANIZATION,
    FooterLink.GROUP_CONTACT,
)


def list_or_default(queryset, fallback):
    items = list(queryset)
    return items or fallback


def site_content(request):
    try:
        settings = SiteSettings.objects.first() or defaults.SITE_SETTINGS
        navigation_items = list(
            NavigationItem.objects.filter(
                is_cta=False,
                is_active=True,
            ).order_by("sort_order", "id")
        )
        navigation_items_before_focus = [
            item for item in navigation_items if item.sort_order < 40
        ] or defaults.NAVIGATION_BEFORE_FOCUS
        navigation_items_after_focus = [
            item for item in navigation_items if item.sort_order >= 40
        ] or defaults.NAVIGATION_AFTER_FOCUS
        footer_links = {
            group: list_or_default(
                FooterLink.objects.filter(group=group, is_active=True).order_by(
                    "sort_order",
                    "id",
                ),
                defaults.FOOTER_LINKS.get(group, []),
            )
            for group in FOOTER_GROUPS
        }
        return {
            "site_settings": settings,
            "navigation_items_before_focus": navigation_items_before_focus,
            "navigation_items_after_focus": navigation_items_after_focus,
            "navigation_ctas": list_or_default(
                NavigationItem.objects.filter(
                    is_cta=True,
                    is_active=True,
                ).order_by("sort_order", "id"),
                defaults.NAVIGATION_CTAS,
            ),
            "focus_area_links": list_or_default(
                FocusArea.objects.filter(is_active=True).order_by(
                    "sort_order",
                    "title",
                ),
                defaults.FOCUS_AREA_LINKS,
            ),
            "footer_links": footer_links,
        }
    except (OperationalError, ProgrammingError):
        return {
            "site_settings": defaults.SITE_SETTINGS,
            "navigation_items_before_focus": defaults.NAVIGATION_BEFORE_FOCUS,
            "navigation_items_after_focus": defaults.NAVIGATION_AFTER_FOCUS,
            "navigation_ctas": defaults.NAVIGATION_CTAS,
            "focus_area_links": defaults.FOCUS_AREA_LINKS,
            "footer_links": defaults.FOOTER_LINKS,
        }
