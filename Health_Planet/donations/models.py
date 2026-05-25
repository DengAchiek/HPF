from django.db import models


class DonationInterest(models.Model):
    STATUS_NEW = "new"
    STATUS_CONTACTED = "contacted"
    STATUS_CLOSED = "closed"
    STATUS_SPAM = "spam"
    STATUS_CHOICES = (
        (STATUS_NEW, "New"),
        (STATUS_CONTACTED, "Contacted"),
        (STATUS_CLOSED, "Closed"),
        (STATUS_SPAM, "Spam"),
    )

    full_name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    amount_selection = models.CharField(max_length=40)
    custom_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=8, default="USD")
    message = models.TextField(blank=True)
    privacy_consent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    admin_notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-submitted_at",)
        verbose_name = "Donation interest"
        verbose_name_plural = "Donation interests"

    def __str__(self):
        return f"{self.full_name} - {self.display_amount}"

    @property
    def display_amount(self):
        if self.amount_selection == "custom" and self.custom_amount:
            return f"{self.currency} {self.custom_amount}"
        return f"{self.currency} {self.amount_selection}"
