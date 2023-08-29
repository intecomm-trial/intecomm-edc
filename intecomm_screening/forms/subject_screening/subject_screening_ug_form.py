from __future__ import annotations

from typing import Type

from django import forms
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin
from edc_sites.modelform_mixins import SiteModelFormMixin
from intecomm_form_validators import SubjectScreeningFormValidator

from ...models import PatientLogUg, SubjectScreeningUg
from .modelform_mixins import SubjectScreeningModelFormMixin


class SubjectScreeningUgForm(
    SubjectScreeningModelFormMixin,
    AlreadyConsentedFormMixin,
    SiteModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    form_validator_cls = SubjectScreeningFormValidator

    @property
    def patient_log_model_cls(self) -> Type[PatientLogUg]:
        return PatientLogUg

    class Meta:
        model = SubjectScreeningUg
        fields = "__all__"
        labels = {
            "consent_ability": "Is the patient able and willing to give informed consent.",
            "site": "Which study site is this?",
        }
        widgets = {
            "patient_log_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
            "legal_name": forms.TextInput(attrs={"readonly": "readonly"}),
            "familiar_name": forms.TextInput(attrs={"readonly": "readonly"}),
            "initials": forms.TextInput(attrs={"readonly": "readonly"}),
            "age_in_years": forms.TextInput(attrs={"readonly": "readonly"}),
            "hospital_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
        help_texts = {
            "patient_log_identifier": "(read-only)",
            "site": "This question is asked to confirm you are logged in to the correct site.",
        }
