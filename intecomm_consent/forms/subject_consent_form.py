from django import forms
from edc_consent.modelform_mixins import ConsentModelFormMixin
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from intecomm_form_validators.consent import SubjectConsentFormValidator

from intecomm_screening.models import SubjectScreening
from intecomm_screening.utils import (
    validate_is_eligible,
    validate_not_already_refused_consent,
    validate_not_screened_despite_unwilling_to_screen,
)

from ..models import SubjectConsent
from ..utils import validate_not_already_consented


class ConsentFormMixin:
    def clean(self):
        cleaned_data = super().clean()
        screening_identifier = cleaned_data.get("screening_identifier")
        if screening_identifier:
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=screening_identifier
            )

            validate_not_screened_despite_unwilling_to_screen(
                subject_screening=subject_screening
            )
            validate_is_eligible(subject_screening=subject_screening)
            validate_not_already_consented(subject_screening=subject_screening)
            validate_not_already_refused_consent(subject_screening=subject_screening)

        return cleaned_data


class SubjectConsentForm(
    ConsentFormMixin,
    SiteModelFormMixin,
    FormValidatorMixin,
    ConsentModelFormMixin,
    forms.ModelForm,
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
