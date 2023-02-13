from django import forms
from edc_form_validators import FormValidatorMixin
from intecomm_form_validators import PatientGroupFormValidator

from ..models import PatientGroup


class PatientGroupForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = PatientGroupFormValidator

    class Meta:
        model = PatientGroup
        fields = "__all__"
