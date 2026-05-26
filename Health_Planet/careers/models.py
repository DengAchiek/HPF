from django.db import models


class ApplicationSubmission(models.Model):
    TYPE_CAREER = "career"
    TYPE_INTERNSHIP = "internship"
    TYPE_CHOICES = (
        (TYPE_CAREER, "Career"),
        (TYPE_INTERNSHIP, "Internship"),
    )
    STATUS_NEW = "new"
    STATUS_REVIEWING = "reviewing"
    STATUS_SHORTLISTED = "shortlisted"
    STATUS_CLOSED = "closed"
    STATUS_SPAM = "spam"
    STATUS_CHOICES = (
        (STATUS_NEW, "New"),
        (STATUS_REVIEWING, "Reviewing"),
        (STATUS_SHORTLISTED, "Shortlisted"),
        (STATUS_CLOSED, "Closed"),
        (STATUS_SPAM, "Spam"),
    )

    application_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    opportunity_label = models.CharField(max_length=180)
    full_name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    location = models.CharField(max_length=160, blank=True)
    cv_link = models.URLField(blank=True)
    cover_message = models.TextField()
    privacy_consent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    admin_notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-submitted_at",)
        verbose_name = "Application"
        verbose_name_plural = "Applications"

    def __str__(self):
        return f"{self.full_name} - {self.opportunity_label}"
