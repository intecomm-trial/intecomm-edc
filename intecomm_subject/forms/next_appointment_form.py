from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_next_appointment.modelform_mixins import NextAppointmentModelFormMixin
from intecomm_form_validators.subject import NextAppointmentFormValidator

from ..models import NextAppointment


class NextAppointmentForm(NextAppointmentModelFormMixin, CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = NextAppointmentFormValidator

    class Meta:
        model = NextAppointment
        fields = "__all__"
        labels = {
            "health_facility": "Health facility or meeting location",
            "appt_date": "Next scheduled appointment date",
        }
        help_texts = {
            "health_facility": "Note: may also be a community group meeting location"
        }
