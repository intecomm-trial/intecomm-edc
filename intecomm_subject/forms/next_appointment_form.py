from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from intecomm_form_validators.subject import NextAppointmentFormValidator

from ..models import NextAppointment


class NextAppointmentForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = NextAppointmentFormValidator

    class Meta:
        model = NextAppointment
        fields = "__all__"
