from django import forms

from .models import ApplicationSubmission


class ApplicationSubmissionForm(forms.ModelForm):
    privacy_consent = forms.BooleanField(
        label=(
            "I consent to Health Planet Foundation using my details to assess this "
            "application and contact me about this opportunity."
        ),
        required=True,
    )
    website = forms.CharField(
        required=False,
        label="Leave this field empty",
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
    )

    class Meta:
        model = ApplicationSubmission
        fields = (
            "opportunity_label",
            "full_name",
            "email",
            "phone",
            "location",
            "cv_link",
            "cover_message",
            "privacy_consent",
        )
        labels = {
            "opportunity_label": "Opportunity",
            "full_name": "Full name",
            "phone": "Phone number (optional)",
            "location": "Current location (optional)",
            "cv_link": "CV or portfolio link (optional)",
            "cover_message": "Why are you interested?",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel"}),
            "location": forms.TextInput(attrs={"autocomplete": "address-level2"}),
            "cv_link": forms.URLInput(attrs={"placeholder": "https://"}),
            "cover_message": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, application_type, opportunities=None, **kwargs):
        super().__init__(*args, **kwargs)
        default_label = (
            "General career application"
            if application_type == ApplicationSubmission.TYPE_CAREER
            else "General internship interest"
        )
        choices = [(default_label, default_label)]
        choices.extend((label, label) for label in opportunities or [])
        self.fields["opportunity_label"] = forms.ChoiceField(
            label="Opportunity",
            choices=choices,
        )
        self.instance.application_type = application_type

    def clean_cover_message(self):
        message = self.cleaned_data["cover_message"].strip()
        if len(message) < 30:
            raise forms.ValidationError(
                "Please briefly describe your interest and relevant experience."
            )
        return message
