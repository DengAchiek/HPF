from django.contrib import admin

from .models import DonationInterest


@admin.register(DonationInterest)
class DonationInterestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "amount_display", "status", "submitted_at")
    list_filter = ("status", "currency", "submitted_at", "privacy_consent")
    search_fields = ("full_name", "email", "phone", "message")
    readonly_fields = (
        "full_name",
        "email",
        "phone",
        "amount_selection",
        "custom_amount",
        "currency",
        "message",
        "privacy_consent",
        "submitted_at",
    )
    fieldsets = (
        (
            "Support enquiry",
            {
                "fields": (
                    "full_name",
                    "email",
                    "phone",
                    "amount_selection",
                    "custom_amount",
                    "currency",
                    "message",
                    "privacy_consent",
                    "submitted_at",
                )
            },
        ),
        ("Handling", {"fields": ("status", "admin_notes")}),
    )

    @admin.display(description="Amount")
    def amount_display(self, obj):
        return obj.display_amount
