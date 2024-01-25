from django import forms
from edc_consent.modelform_mixins import ConsentModelFormMixin
from edc_form_validators import FormValidatorMixin
from edc_screening.utils import is_eligible_or_raise
from edc_sites.forms import SiteModelFormMixin
from intecomm_form_validators.consent import SubjectConsentFormValidator

from intecomm_screening.utils import raise_if_consent_refusal_exists


class SubjectConsentModelFormMixin(
    SiteModelFormMixin,
    FormValidatorMixin,
    ConsentModelFormMixin,
):
    form_validator_cls = SubjectConsentFormValidator

    screening_identifier = forms.CharField(
        label="Screening identifier",
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    def clean(self):
        raise_if_consent_refusal_exists(
            self.cleaned_data.get("screening_identifier"), is_modelform=True
        )
        return super().clean()

    def validate_guardian_and_dob(self):
        """Override method from modelform"""
        pass

    def clean_guardian_and_dob(self):
        """Override method from form validator"""
        pass

    def validate_is_eligible_or_raise(self) -> None:
        screening_identifier = self.get_field_or_raise(
            "screening_identifier", "Screening identifier is required."
        )
        is_eligible_or_raise(
            screening_identifier=screening_identifier,
            url_name="intecomm_screening_admin:intecomm_screening_patientlog_changelist",
        )

    class Meta:
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
