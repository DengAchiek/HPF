from django.contrib import admin

from .models import (
    CareerOpening,
    DonationAmount,
    FeatureCard,
    FocusArea,
    FooterLink,
    GalleryImage,
    InternshipTrack,
    NavigationItem,
    NewsItem,
    PageContent,
    Project,
    SectionContent,
    SiteSettings,
    StatItem,
    TeamMember,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Brand", {"fields": ("organization_name", "tagline", "logo", "static_logo")}),
        ("Navigation", {"fields": ("focus_dropdown_label",)}),
        (
            "Footer and Contact",
            {
                "fields": (
                    "footer_about",
                    "contact_name",
                    "location",
                    "email",
                    "phone",
                    "copyright_text",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ("label", "url_name", "external_url", "is_cta", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_cta", "is_active")


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "group", "url_name", "external_url", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("group", "is_active")


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "hero_kicker", "hero_class")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Page", {"fields": ("title", "slug", "meta_title")}),
        ("Hero", {"fields": ("hero_class", "hero_kicker", "hero_title", "hero_text")}),
        ("Hero Image", {"fields": ("image", "static_image", "image_alt")}),
    )


@admin.register(SectionContent)
class SectionContentAdmin(admin.ModelAdmin):
    list_display = ("page_slug", "key", "kicker", "title")
    list_filter = ("page_slug",)
    search_fields = ("key", "title", "body")
    fieldsets = (
        ("Placement", {"fields": ("page_slug", "key")}),
        ("Content", {"fields": ("kicker", "title", "body")}),
        ("Button", {"fields": ("button_label", "button_url_name", "button_external_url")}),
        ("Image", {"fields": ("image", "static_image", "image_alt", "image_caption")}),
    )


@admin.register(FeatureCard)
class FeatureCardAdmin(admin.ModelAdmin):
    list_display = ("title", "section_key", "icon", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("section_key", "is_active")


@admin.register(StatItem)
class StatItemAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "description", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("title", "description", "status")


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "date_label", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("title", "summary")


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("caption", "gallery_key", "focus_class", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("gallery_key", "is_active")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "team", "photo_pending", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("team", "photo_pending", "is_active")
    search_fields = ("name", "role", "bio")


@admin.register(FocusArea)
class FocusAreaAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "points_text")


@admin.register(CareerOpening)
class CareerOpeningAdmin(admin.ModelAdmin):
    list_display = ("role", "location", "employment_type", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")


@admin.register(InternshipTrack)
class InternshipTrackAdmin(admin.ModelAdmin):
    list_display = ("role", "icon", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")


@admin.register(DonationAmount)
class DonationAmountAdmin(admin.ModelAdmin):
    list_display = ("amount", "label", "select_value", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
