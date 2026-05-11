from django.db.utils import OperationalError, ProgrammingError

from .models import FocusArea, FooterLink, NavigationItem, SiteSettings


def site_content(request):
    try:
        settings = SiteSettings.load()
        navigation_items = list(
            NavigationItem.objects.filter(
                is_cta=False,
                is_active=True,
            ).order_by("sort_order", "id")
        )
        footer_links = {
            group: list(
                FooterLink.objects.filter(group=group, is_active=True).order_by("sort_order", "id")
            )
            for group in (
                FooterLink.GROUP_PROGRAMS,
                FooterLink.GROUP_ORGANIZATION,
                FooterLink.GROUP_CONTACT,
            )
        }
        return {
            "site_settings": settings,
            "navigation_items_before_focus": [
                item for item in navigation_items if item.sort_order < 40
            ],
            "navigation_items_after_focus": [
                item for item in navigation_items if item.sort_order >= 40
            ],
            "navigation_ctas": list(
                NavigationItem.objects.filter(
                    is_cta=True,
                    is_active=True,
                ).order_by("sort_order", "id")
            ),
            "focus_area_links": list(
                FocusArea.objects.filter(is_active=True).order_by(
                    "sort_order",
                    "title",
                )
            ),
            "footer_links": footer_links,
        }
    except (OperationalError, ProgrammingError):
        return {
            "site_settings": SiteSettings(),
            "navigation_items_before_focus": [],
            "navigation_items_after_focus": [],
            "navigation_ctas": [],
            "focus_area_links": [],
            "footer_links": {},
        }
