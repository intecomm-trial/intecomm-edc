from django import forms
from edc_form_validators import FormValidatorMixin
from intecomm_form_validators import PatientGroupScreeningFormValidator

from ..models import PatientGroup


class PatientGroupForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = PatientGroupScreeningFormValidator

    class Meta:
        model = PatientGroup
        fields = "__all__"
