from django import forms
from edc_form_validators import FormValidatorMixin
from intecomm_form_validators import PatientCallFormValidator

from ..models import PatientCall


class PatientCallForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = PatientCallFormValidator

    class Meta:
        model = PatientCall
        fields = "__all__"
