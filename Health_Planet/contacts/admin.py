from django.contrib import admin

from .models import ContactSubmission


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "organization", "status", "submitted_at")
    list_filter = ("status", "submitted_at", "privacy_consent")
    search_fields = ("full_name", "email", "phone", "organization", "message")
    readonly_fields = (
        "full_name",
        "email",
        "phone",
        "organization",
        "message",
        "privacy_consent",
        "submitted_at",
    )
    fieldsets = (
        (
            "Enquiry",
            {
                "fields": (
                    "full_name",
                    "email",
                    "phone",
                    "organization",
                    "message",
                    "privacy_consent",
                    "submitted_at",
                )
            },
        ),
        ("Handling", {"fields": ("status", "admin_notes")}),
    )
