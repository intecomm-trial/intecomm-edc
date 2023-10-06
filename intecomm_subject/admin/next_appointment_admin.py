from django.contrib import admin
from edc_appointment.modeladmin_mixins import NextAppointmentCrfModelAdminMixin
from edc_constants.constants import INTEGRATED
from edc_facility.utils import get_health_facility_model_cls

from ..admin_site import intecomm_subject_admin
from ..forms import NextAppointmentForm
from ..models import NextAppointment
from .modeladmin_mixins import CrfModelAdmin


@admin.register(NextAppointment, site=intecomm_subject_admin)
class NextAppointmentAdmin(NextAppointmentCrfModelAdminMixin, CrfModelAdmin):
    form = NextAppointmentForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "health_facility":
            kwargs["queryset"] = get_health_facility_model_cls().on_site.filter(
                health_facility_type__name__in=[INTEGRATED]
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
