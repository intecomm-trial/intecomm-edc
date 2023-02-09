from django import forms
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin
from edc_sites.modelform_mixins import SiteModelFormMixin
from intecomm_form_validators import PatientLogFormValidator

from ..models import PatientLog


class PatientLogForm(
    AlreadyConsentedFormMixin, SiteModelFormMixin, FormValidatorMixin, forms.ModelForm
):
    form_validator_cls = PatientLogFormValidator

    class Meta:
        model = PatientLog
        fields = "__all__"
