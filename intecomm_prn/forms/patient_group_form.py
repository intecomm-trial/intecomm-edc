from django import forms

from intecomm_screening.forms import PatientGroupForm as Base

from ..models import PatientGroup


class PatientGroupForm(Base, forms.ModelForm):

    form_validator_cls = None

    class Meta:
        model = PatientGroup
        fields = "__all__"
