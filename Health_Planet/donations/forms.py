from decimal import Decimal

from django import forms

from .models import DonationInterest


class DonationInterestForm(forms.ModelForm):
    privacy_consent = forms.BooleanField(
        label=(
            "I consent to Health Planet Foundation using my details to contact me about giving."
        ),
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
        model = DonationInterest
        fields = (
            "full_name",
            "email",
            "phone",
            "amount_selection",
            "custom_amount",
            "message",
            "privacy_consent",
        )
        labels = {
            "full_name": "Full name",
            "phone": "Phone number (optional)",
            "amount_selection": "Preferred contribution amount",
            "custom_amount": "Custom amount (USD)",
            "message": "Note (optional)",
            "privacy_consent": (
                "I consent to Health Planet Foundation using my details to contact me about giving."
            ),
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel"}),
            "custom_amount": forms.NumberInput(attrs={"min": "1", "step": "0.01"}),
            "message": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, amounts=None, **kwargs):
        super().__init__(*args, **kwargs)
        amount_options = [
            (amount.select_value, f"USD {amount.amount} - {amount.label}")
            for amount in amounts or []
        ]
        self.fields["amount_selection"] = forms.ChoiceField(
            label="Preferred contribution amount",
            choices=[("", "Select an amount"), *amount_options, ("custom", "Custom amount")],
        )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("amount_selection") == "custom":
            amount = cleaned_data.get("custom_amount")
            if not amount:
                self.add_error("custom_amount", "Enter the amount you would like to contribute.")
            elif amount <= Decimal("0"):
                self.add_error("custom_amount", "Enter an amount greater than zero.")
        else:
            cleaned_data["custom_amount"] = None
        return cleaned_data
