from django.core import mail
from django.test import TestCase, override_settings

from .models import ContactSubmission


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    CONTACT_NOTIFICATION_EMAIL="programs@example.org",
    DEFAULT_FROM_EMAIL="website@example.org",
)
class ContactSubmissionTests(TestCase):
    def valid_submission(self):
        return {
            "full_name": "Mary Banda",
            "email": "mary@example.org",
            "phone": "+260 971 000000",
            "organization": "Community Health Group",
            "message": "I would like to discuss a partnership for community outreach.",
            "privacy_consent": "on",
        }

    def test_valid_enquiry_is_stored_and_notifies_team(self):
        response = self.client.post("/contact/", self.valid_submission(), follow=True)

        self.assertRedirects(response, "/contact/")
        self.assertContains(response, "Your message has been received")
        submission = ContactSubmission.objects.get()
        self.assertEqual(submission.full_name, "Mary Banda")
        self.assertTrue(submission.privacy_consent)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Mary Banda", mail.outbox[0].body)

    def test_privacy_consent_is_required(self):
        data = self.valid_submission()
        data.pop("privacy_consent")

        response = self.client.post("/contact/", data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        self.assertFalse(ContactSubmission.objects.exists())

    def test_honeypot_submission_is_not_stored(self):
        response = self.client.post(
            "/contact/",
            {"website": "https://spam.example"},
            follow=True,
        )

        self.assertContains(response, "Your message has been received")
        self.assertFalse(ContactSubmission.objects.exists())
        self.assertEqual(len(mail.outbox), 0)
