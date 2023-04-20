from django import forms
from django.conf import settings
from edc_appointment.exceptions import AppointmentWindowError
from edc_appointment.utils import raise_on_appt_datetime_not_in_window
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_utils import convert_php_dateformat, to_utc
from intecomm_form_validators.subject import NextAppointmentFormValidator

from ..models import NextAppointment


class NextAppointmentForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = NextAppointmentFormValidator

    def clean(self):
        cleaned_data = super().clean()
        self.validate_best_visit_code()
        return cleaned_data

    def validate_best_visit_code(self):
        if appt_date := self.cleaned_data.get("appt_date"):
            subject_visit = self.cleaned_data.get("subject_visit")
            appointment = subject_visit.appointment.next
            while appointment:
                if appt_date <= to_utc(appointment.appt_datetime).date():
                    break
                appointment = appointment.next
            # is after appointment.previous and before appointment
            try:
                raise_on_appt_datetime_not_in_window(appointment)
            except AppointmentWindowError:
                appointment = appointment.previous
            if self.cleaned_data.get("best_visit_code") != appointment.visit_code:
                date_format = convert_php_dateformat(settings.SHORT_DATE_FORMAT)
                raise forms.ValidationError(
                    {
                        "best_visit_code": (
                            f"Expected {appointment.visit_code} "
                            f"using {appt_date.strftime(date_format)} from above."
                        )
                    }
                )

    class Meta:
        model = NextAppointment
        fields = "__all__"
