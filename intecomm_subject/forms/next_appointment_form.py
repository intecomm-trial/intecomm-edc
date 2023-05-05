from datetime import date, datetime
from zoneinfo import ZoneInfo

from django import forms
from django.conf import settings
from edc_appointment.utils import (
    AppointmentDateWindowPeriodGapError,
    get_appointment_by_datetime,
)
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_utils import convert_php_dateformat
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
            try:
                appointment = get_appointment_by_datetime(
                    self.as_appt_datetime(appt_date),
                    subject_identifier=subject_visit.subject_identifier,
                    visit_schedule_name=subject_visit.visit_schedule.name,
                    schedule_name=subject_visit.schedule.name,
                )
            except AppointmentDateWindowPeriodGapError as e:
                raise forms.ValidationError({"appt_date": str(e)})
            if not appointment:
                raise forms.ValidationError(
                    {"appt_date": "Invalid. Must be within the followup period."}
                )
            elif appointment == subject_visit.appointment:
                raise forms.ValidationError(
                    {
                        "appt_date": (
                            "Invalid. Cannot be within window period of current appointment."
                        )
                    }
                )

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

    @staticmethod
    def as_appt_datetime(appt_date: date) -> datetime:
        return datetime(
            appt_date.year,
            appt_date.month,
            appt_date.day,
            0,
            0,
            0,
            tzinfo=ZoneInfo("UTC"),
        )

    class Meta:
        model = NextAppointment
        fields = "__all__"
