from django.core import mail
from django.test import TestCase, override_settings

from core.models import DonationAmount

from .models import DonationInterest


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DONATION_NOTIFICATION_EMAIL="giving@example.org",
    DEFAULT_FROM_EMAIL="website@example.org",
)
class DonationInterestTests(TestCase):
    def setUp(self):
        DonationAmount.objects.create(
            amount="50.00",
            label="Community session support",
            select_value="50",
            is_active=True,
        )

    def valid_submission(self):
        return {
            "full_name": "John Phiri",
            "email": "john@example.org",
            "phone": "+260 972 000000",
            "amount_selection": "50",
            "message": "Please contact me with approved giving options.",
            "privacy_consent": "on",
        }

    def test_valid_interest_is_stored_and_notifies_team(self):
        response = self.client.post("/donate/", self.valid_submission(), follow=True)

        self.assertRedirects(response, "/donate/")
        self.assertContains(response, "support interest has been received")
        submission = DonationInterest.objects.get()
        self.assertEqual(submission.amount_selection, "50")
        self.assertEqual(submission.display_amount, "USD 50")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("USD 50", mail.outbox[0].body)

    def test_custom_amount_is_required_when_selected(self):
        data = self.valid_submission()
        data["amount_selection"] = "custom"

        response = self.client.post("/donate/", data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter the amount you would like to contribute")
        self.assertFalse(DonationInterest.objects.exists())

    def test_unlisted_amount_is_rejected(self):
        data = self.valid_submission()
        data["amount_selection"] = "100000"

        response = self.client.post("/donate/", data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select a valid choice")
        self.assertFalse(DonationInterest.objects.exists())

    def test_custom_amount_must_be_positive(self):
        data = self.valid_submission()
        data.update({"amount_selection": "custom", "custom_amount": "-5"})

        response = self.client.post("/donate/", data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter an amount greater than zero")
        self.assertFalse(DonationInterest.objects.exists())

    def test_honeypot_submission_is_not_stored(self):
        response = self.client.post(
            "/donate/",
            {"website": "https://spam.example"},
            follow=True,
        )

        self.assertContains(response, "support interest has been received")
        self.assertFalse(DonationInterest.objects.exists())
        self.assertEqual(len(mail.outbox), 0)
