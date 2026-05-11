from django.test import TestCase

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
