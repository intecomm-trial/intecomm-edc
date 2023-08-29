from django import forms
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin
from edc_sites.modelform_mixins import SiteModelFormMixin
from intecomm_form_validators import PatientLogFormValidator

from ...models import PatientLogUg
from .patient_log_form import PatientLogFormMixin


class PatientLogUgForm(
    PatientLogFormMixin,
    AlreadyConsentedFormMixin,
    SiteModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    form_validator_cls = PatientLogFormValidator

    class Meta:
        model = PatientLogUg
        fields = "__all__"
        exclude = ["legal_name", "familiar_name"]
