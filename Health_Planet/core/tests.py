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
    NewsImage,
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
    def hero_markup(self, response, section_class):
        html = response.content.decode()
        hero_start = html.split(f'<section class="{section_class}', 1)[1]
        return hero_start.split("</section>", 1)[0]

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
        self.assertContains(
            response,
            "/news/rana-bootcamp-advances-epidemic-preparedness-across-africa/",
        )
        self.assertContains(response, "Read update")
        self.assertNotContains(response, "The Tribe Hotel, Nairobi, Kenya")
        self.assertNotContains(response, "Intercontinental Hotel, Lusaka, Zambia")
        self.assertContains(response, "healthyplanetfoundation@gmail.com")
        self.assertContains(response, 'class="photo-sequence"', count=4)

    def test_hero_carousels_use_page_specific_images(self):
        home_response = self.client.get("/")
        home_hero = self.hero_markup(home_response, "home-hero")

        self.assertIn("images/im-02.jpeg", home_hero)
        self.assertIn("images/im-12.jpeg", home_hero)
        self.assertNotIn("images/news/rana-bootcamp-2026.jpg", home_hero)
        self.assertNotIn("images/im-18.jpeg", home_hero)

        news_response = self.client.get("/news/")
        news_hero = self.hero_markup(news_response, "page-hero hero-news")

        self.assertIn("images/news/rana-bootcamp-2026.jpg", news_hero)
        self.assertIn("images/news/continental-conference-lusaka-2026.jpg", news_hero)
        self.assertNotIn("images/im-02.jpeg", news_hero)

    def test_admin_hero_gallery_is_scoped_to_its_page(self):
        GalleryImage.objects.create(
            gallery_key="about_hero",
            static_image="images/im-08.jpeg",
            image_alt="About hero custom field image",
            is_active=True,
        )
        GalleryImage.objects.create(
            gallery_key="home_hero",
            static_image="images/im-02.jpeg",
            image_alt="Home hero custom field image",
            is_active=True,
        )

        response = self.client.get("/about/")
        about_hero = self.hero_markup(response, "page-hero hero-about")

        self.assertIn("images/im-08.jpeg", about_hero)
        self.assertNotIn("images/im-02.jpeg", about_hero)

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
        plain_item = NewsItem.objects.create(
            title="Admin news without event details",
            summary="This update can be saved with only the required news fields.",
            is_active=True,
            sort_order=1,
        )
        detailed_item = NewsItem.objects.create(
            title="Admin news with event details",
            summary="This update includes the optional event details.",
            body="The first paragraph gives readers more context.\n\nThe second paragraph adds detail.",
            date_label="1 May 2026",
            event_date=date(2026, 5, 1),
            venue="Lusaka, Zambia",
            participants="Community health partners",
            is_active=True,
            sort_order=2,
        )
        NewsImage.objects.create(
            news_item=detailed_item,
            static_image="images/im-01.jpeg",
            image_alt="Community gathering",
            caption="Community partners in session",
            is_active=True,
            sort_order=1,
        )

        response = self.client.get("/news/")

        self.assertContains(response, "Admin news without event details")
        self.assertContains(response, "Admin news with event details")
        self.assertContains(response, plain_item.detail_href)
        self.assertContains(response, detailed_item.detail_href)
        self.assertContains(response, "Read More")
        self.assertContains(response, "1 May 2026")
        self.assertContains(response, "Lusaka, Zambia")
        self.assertNotContains(response, "None")

        detail_response = self.client.get(detailed_item.detail_href)

        self.assertContains(detail_response, "Admin news with event details")
        self.assertContains(detail_response, "Community health partners")
        self.assertContains(detail_response, "The first paragraph gives readers more context.")
        self.assertContains(detail_response, "The second paragraph adds detail.")
        self.assertContains(detail_response, "images/im-01.jpeg")

    def test_default_news_detail_uses_seeded_article_content(self):
        response = self.client.get(
            "/news/rana-bootcamp-advances-epidemic-preparedness-across-africa/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "RANA Bootcamp advances epidemic preparedness across Africa")
        self.assertContains(response, "community-engaged disease surveillance")
        self.assertContains(response, "images/news/rana-bootcamp-2026.jpg")
        self.assertContains(response, "images/news/rana-bootcamp-2026-group.jpg")
