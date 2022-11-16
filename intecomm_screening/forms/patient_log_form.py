from django import forms
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin
from edc_sites.modelform_mixins import SiteModelFormMixin
from edc_sites.widgets import SiteField
from intecomm_form_validators import PatientLogFormValidator

from ..models import PatientLog


class PatientLogForm(
    AlreadyConsentedFormMixin, SiteModelFormMixin, FormValidatorMixin, forms.ModelForm
):

    form_validator_cls = PatientLogFormValidator

    site = SiteField(label="Health facility")

    class Meta:
        model = PatientLog
        fields = "__all__"
