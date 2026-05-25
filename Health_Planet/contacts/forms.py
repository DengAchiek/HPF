from django import forms

from .models import ContactSubmission


class ContactSubmissionForm(forms.ModelForm):
    privacy_consent = forms.BooleanField(
        label="I consent to Health Planet Foundation using my details to respond to this enquiry.",
        required=True,
    )
    website = forms.CharField(
        required=False,
        label="Leave this field empty",
        widget=forms.TextInput(
            attrs={
                "tabindex": "-1",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = ContactSubmission
        fields = (
            "full_name",
            "email",
            "phone",
            "organization",
            "message",
            "privacy_consent",
        )
        labels = {
            "full_name": "Full name",
            "phone": "Phone number (optional)",
            "organization": "Organization (optional)",
            "privacy_consent": (
                "I consent to Health Planet Foundation using my details to respond to this enquiry."
            ),
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel"}),
            "organization": forms.TextInput(attrs={"autocomplete": "organization"}),
            "message": forms.Textarea(attrs={"rows": 6}),
        }

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("Please provide a little more detail in your message.")
        return message
