from datetime import date

from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

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
    PartnerLogo,
    Project,
    SectionContent,
    SiteSettings,
    StatItem,
    TeamMember,
)


class PublicContentFallbackTests(TestCase):
    def setUp(self):
        for model in (
            SiteSettings,
            NavigationItem,
            FooterLink,
            PageContent,
            SectionContent,
            FeatureCard,
            StatItem,
            Project,
            NewsItem,
            GalleryImage,
            TeamMember,
            FocusArea,
            CareerOpening,
            InternshipTrack,
            DonationAmount,
        ):
            model.objects.all().delete()

    def test_home_uses_default_content_when_admin_content_is_empty(self):
        response = self.client.get("/")

        self.assertContains(response, "Health Planet Foundation")
        self.assertContains(response, "What we do")
        self.assertContains(response, "CLIMATE RESILIENCE &amp; AGRICULTURE")
        self.assertContains(response, "Waste Segregation &amp; Management")
        self.assertContains(response, "ADVOCACY &amp; HEALTH PROMOTIONS")
        self.assertContains(response, "Our partners")
        self.assertContains(response, "Ministry of Health logo")
        self.assertContains(response, "RANA logo")
        self.assertContains(response, "Resolve to Save Lives logo")
        self.assertContains(response, "Thrive Aid logo")
        self.assertContains(response, "Ministry of Green Economy and Environment logo")
        self.assertContains(response, "RANA Bootcamp advances epidemic preparedness across Africa")
        self.assertContains(response, "The Tribe Hotel, Nairobi, Kenya")
        self.assertContains(response, "Intercontinental Hotel, Lusaka, Zambia")
        self.assertContains(response, "healthyplanetfoundation@gmail.com")

    def test_focus_area_uses_default_content_when_admin_content_is_empty(self):
        response = self.client.get("/focus-areas/wash/")

        self.assertContains(response, "WASH")
        self.assertContains(response, "Water safety demonstrations")

    def test_about_team_uses_staff_directory_defaults(self):
        response = self.client.get("/about/")

        self.assertContains(response, "Liyoka Liyoka")
        self.assertContains(response, "Tawanda Nyandoro")
        self.assertContains(response, "images/staff/liyoka-liyoka.jpg")
        self.assertContains(response, "images/staff/tawanda-nyandoro.jpg")
        self.assertNotContains(response, "Photo pending")

    def test_partner_logo_proxy_targets_home_partners(self):
        from .admin import PartnerLogoAdmin

        logo = PartnerLogo(
            caption="Admin Partner",
            static_image="images/partners/admin-partner.png",
        )
        request = RequestFactory().post("/admin/core/partnerlogo/add/")
        PartnerLogoAdmin(PartnerLogo, AdminSite()).save_model(request, logo, form=None, change=False)

        logo.refresh_from_db()
        self.assertEqual(logo.gallery_key, "home_partners")
        response = self.client.get("/")
        self.assertContains(response, "Admin Partner")

    def test_admin_page_content_overrides_default_content(self):
        PageContent.objects.create(
            slug="home",
            title="Home",
            meta_title="Admin Home",
            hero_kicker="Admin managed",
            hero_title="Admin controlled home",
            hero_text="This text came from the Django admin.",
        )

        response = self.client.get("/")

        self.assertContains(response, "Admin controlled home")
        self.assertNotContains(
            response,
            '<h1 id="home-title">Health Planet Foundation</h1>',
        )

    def test_news_event_details_are_optional_and_render_when_present(self):
        NewsItem.objects.create(
            title="Admin news without event details",
            summary="This update can be saved with only the required news fields.",
            is_active=True,
            sort_order=1,
        )
        NewsItem.objects.create(
            title="Admin news with event details",
            summary="This update includes the optional event details.",
            date_label="1 May 2026",
            event_date=date(2026, 5, 1),
            venue="Lusaka, Zambia",
            participants="Community health partners",
            is_active=True,
            sort_order=2,
        )

        response = self.client.get("/news/")

        self.assertContains(response, "Admin news without event details")
        self.assertContains(response, "Admin news with event details")
        self.assertContains(response, "1 May 2026")
        self.assertContains(response, "Lusaka, Zambia")
        self.assertContains(response, "Community health partners")
        self.assertNotContains(response, "None")
