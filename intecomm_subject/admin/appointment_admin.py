from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from edc_appointment.admin import AppointmentAdmin as BaseAdmin
from edc_appointment.admin_site import edc_appointment_admin
from edc_appointment.constants import SKIPPED_APPT
from edc_appointment.form_validators import (
    AppointmentFormValidator as BaseFormValidator,
)
from edc_appointment.forms import AppointmentForm as BaseForm
from edc_appointment.models import Appointment
from edc_appointment.utils import get_allow_skipped_appt_using
from edc_form_validators import INVALID_ERROR
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM
from intecomm_rando.utils import get_assignment_for_subject

edc_appointment_admin.unregister(Appointment)


class AppointmentFormValidator(BaseFormValidator):
    def validate_appt_type(self):
        """Community arm may not skip appointments."""
        if (
            get_assignment_for_subject(self.instance.subject_identifier) == COMMUNITY_ARM
            and self.cleaned_data.get("appt_status") == SKIPPED_APPT
        ):
            self.raise_validation_error(
                {"appt_status": _("Invalid. Community appointments may not be skipped")},
                INVALID_ERROR,
            )
        super().validate_appt_type()


class AppointmentForm(BaseForm):
    form_validator_cls = AppointmentFormValidator


@admin.register(Appointment, site=edc_appointment_admin)
class AppointmentAdmin(BaseAdmin):
    form = AppointmentForm

    def allow_skipped_appointments(self, request) -> bool:
        """Return True only if the subject is in the facility arm."""
        allow = False
        if get_allow_skipped_appt_using():
            try:
                get_assignment_for_subject(
                    request.GET.get("subject_identifier")
                ) == FACILITY_ARM
            except ObjectDoesNotExist:
                pass
            else:
                allow = True
        return allow
