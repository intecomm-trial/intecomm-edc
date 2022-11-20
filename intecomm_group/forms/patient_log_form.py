from django import forms
from edc_form_validators import FormValidatorMixin
from edc_sites.modelform_mixins import SiteModelFormMixin

from ..models import PatientLog


class PatientLogForm(
    SiteModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    class Meta:
        fields = "__all__"
        model = PatientLog
