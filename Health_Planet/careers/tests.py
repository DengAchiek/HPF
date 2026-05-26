from django.core import mail
from django.test import TestCase, override_settings

from core.models import CareerOpening, InternshipTrack

from .models import ApplicationSubmission


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    APPLICATION_NOTIFICATION_EMAIL="recruitment@example.org",
    DEFAULT_FROM_EMAIL="website@example.org",
)
class ApplicationWorkflowTests(TestCase):
    def setUp(self):
        CareerOpening.objects.all().delete()
        InternshipTrack.objects.all().delete()
        CareerOpening.objects.create(
            role="Community Program Officer",
            location="Lusaka",
            employment_type="Full time",
            is_active=True,
        )
        InternshipTrack.objects.create(
            role="Public Health Intern",
            focus="Community sessions and reporting",
            is_active=True,
        )

    def valid_career_submission(self):
        return {
            "opportunity_label": "Community Program Officer",
            "full_name": "Chanda Tembo",
            "email": "chanda@example.org",
            "phone": "+260 973 000000",
            "location": "Lusaka",
            "cv_link": "https://example.org/cv/chanda",
            "cover_message": (
                "I have experience supporting community health outreach and would "
                "like to contribute to local program delivery."
            ),
            "privacy_consent": "on",
        }

    def test_career_page_links_to_application_form(self):
        response = self.client.get("/careers/")

        self.assertContains(response, "/careers/apply/?opportunity=Community%20Program%20Officer")
        form_response = self.client.get(
            "/careers/apply/",
            {"opportunity": "Community Program Officer"},
        )
        self.assertContains(form_response, "Submit application")
        self.assertContains(form_response, "Community Program Officer")

    def test_valid_career_application_is_saved_and_notified(self):
        response = self.client.post(
            "/careers/apply/",
            self.valid_career_submission(),
            follow=True,
        )

        self.assertRedirects(response, "/careers/apply/")
        self.assertContains(response, "Your application has been received")
        application = ApplicationSubmission.objects.get()
        self.assertEqual(application.application_type, ApplicationSubmission.TYPE_CAREER)
        self.assertEqual(application.opportunity_label, "Community Program Officer")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Chanda Tembo", mail.outbox[0].body)

    def test_valid_internship_application_is_saved(self):
        data = self.valid_career_submission()
        data["opportunity_label"] = "Public Health Intern"

        response = self.client.post("/internships/apply/", data, follow=True)

        self.assertRedirects(response, "/internships/apply/")
        application = ApplicationSubmission.objects.get()
        self.assertEqual(application.application_type, ApplicationSubmission.TYPE_INTERNSHIP)

    def test_unlisted_opportunity_and_missing_consent_are_rejected(self):
        data = self.valid_career_submission()
        data["opportunity_label"] = "Invented Position"
        data.pop("privacy_consent")

        response = self.client.post("/careers/apply/", data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select a valid choice")
        self.assertContains(response, "This field is required")
        self.assertFalse(ApplicationSubmission.objects.exists())

    def test_honeypot_application_is_acknowledged_without_storage(self):
        response = self.client.post(
            "/careers/apply/",
            {"website": "https://spam.example"},
            follow=True,
        )

        self.assertContains(response, "Your application has been received")
        self.assertFalse(ApplicationSubmission.objects.exists())
        self.assertEqual(len(mail.outbox), 0)
