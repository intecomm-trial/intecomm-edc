from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from edc_consent.modelform_mixins import ConsentModelFormMixin
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from intecomm_form_validators.consent import SubjectConsentFormValidator

from intecomm_screening.models import SubjectScreening
from intecomm_screening.utils import (
    AlreadyRefusedConsentError,
    MultipleConsentRefusalsDetectedError,
    get_add_or_change_refusal_url,
    raise_if_already_refused_consent,
)

from ..models import SubjectConsent


class ConsentFormMixin:
    def clean(self):
        cleaned_data = super().clean()
        screening_identifier = cleaned_data.get("screening_identifier")
        if screening_identifier:
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=screening_identifier
            )

            self.validate_not_already_refused_consent(subject_screening=subject_screening)

        return cleaned_data

    @staticmethod
    def validate_not_already_refused_consent(subject_screening: SubjectScreening) -> None:
        try:
            raise_if_already_refused_consent(
                screening_identifier=subject_screening.screening_identifier
            )
        except AlreadyRefusedConsentError:
            _, consent_refusal_url = get_add_or_change_refusal_url(obj=subject_screening)
            msg = format_html(
                "Not allowed. Patient has already refused consent. "
                'See subject <A href="{}">{}</A>',
                mark_safe(consent_refusal_url),  # nosec B308 B703
                subject_screening.screening_identifier,
            )
            raise forms.ValidationError(msg)
        except MultipleConsentRefusalsDetectedError:
            raise forms.ValidationError(
                "Not allowed. Multiple consents refusals detected "
                f"for subject '{subject_screening.screening_identifier}'. "
                "Inform data manager before continuing."
            )


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
