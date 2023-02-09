from django import forms
from edc_consent.modelform_mixins import ConsentModelFormMixin
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from intecomm_form_validators.consent import SubjectConsentFormValidator

from ..models import SubjectConsent


class SubjectConsentForm(
    SiteModelFormMixin, FormValidatorMixin, ConsentModelFormMixin, forms.ModelForm
):
    form_validator_cls = SubjectConsentFormValidator

    screening_identifier = forms.CharField(
        label="Screening identifier",
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    def validate_guardian_and_dob(self):
        """Override method from modelform"""
        pass

    def clean_guardian_and_dob(self):
        """Override method from form validator"""
        return None

    class Meta:
        model = SubjectConsent
        fields = "__all__"
        help_texts = {
            "identity": (
                "Use Country ID Number, Passport number, driver's license "
                "number or Country ID receipt number"
            ),
            "witness_name": (
                "Required only if participant is illiterate. "
                "Format is 'LASTNAME, FIRSTNAME'. "
                "All uppercase separated by a comma."
            ),
        }
        widgets = {
            "legal_name": forms.TextInput(attrs={"readonly": "readonly"}),
            "familiar_name": forms.TextInput(attrs={"readonly": "readonly"}),
            "initials": forms.TextInput(attrs={"readonly": "readonly"}),
            "identity": forms.TextInput(attrs={"readonly": "readonly"}),
        }
