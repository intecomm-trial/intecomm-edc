from django import forms
from edc_form_validators import FormValidatorMixin
from intecomm_form_validators import PatientCallFormValidator

from ..models import PatientFollowupCall


class PatientFollowupCallForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = PatientCallFormValidator

    class Meta:
        model = PatientFollowupCall
        fields = "__all__"
