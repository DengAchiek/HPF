from django.contrib import admin

from .models import ApplicationSubmission


@admin.register(ApplicationSubmission)
class ApplicationSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "application_type",
        "opportunity_label",
        "status",
        "submitted_at",
    )
    list_filter = ("application_type", "status", "submitted_at", "privacy_consent")
    search_fields = (
        "full_name",
        "email",
        "phone",
        "location",
        "opportunity_label",
        "cover_message",
    )
    readonly_fields = (
        "application_type",
        "opportunity_label",
        "full_name",
        "email",
        "phone",
        "location",
        "cv_link",
        "cover_message",
        "privacy_consent",
        "submitted_at",
    )
    fieldsets = (
        (
            "Candidate submission",
            {
                "fields": (
                    "application_type",
                    "opportunity_label",
                    "full_name",
                    "email",
                    "phone",
                    "location",
                    "cv_link",
                    "cover_message",
                    "privacy_consent",
                    "submitted_at",
                )
            },
        ),
        ("Review", {"fields": ("status", "admin_notes")}),
    )
