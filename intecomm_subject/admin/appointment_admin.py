from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from edc_appointment.admin import AppointmentAdmin as BaseAdmin
from edc_appointment.admin_site import edc_appointment_admin
from edc_appointment.models import Appointment, AppointmentType
from edc_appointment.utils import get_allow_skipped_appt_using
from edc_constants.constants import HOSPITAL, NOT_APPLICABLE
from intecomm_rando.constants import FACILITY_ARM
from intecomm_rando.utils import get_assignment_for_subject

from ..forms import AppointmentForm
from .list_filters import PatientGroupListFilter

edc_appointment_admin.unregister(Appointment)


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

    def get_appt_type_queryset(self, request) -> QuerySet:
        if not self.allow_skipped_appointments(request):
            return AppointmentType.objects.exclude(
                name__in=[HOSPITAL, NOT_APPLICABLE]
            ).order_by("display_index")
        return AppointmentType.objects.exclude(name__in=[HOSPITAL]).order_by("display_index")

    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        list_filter = list_filter + (PatientGroupListFilter,)
        return list_filter
