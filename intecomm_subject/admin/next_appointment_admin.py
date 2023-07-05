from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from intecomm_screening.models import HealthFacility

from ..admin_site import intecomm_subject_admin
from ..constants import INTEGRATED
from ..forms import NextAppointmentForm
from ..models import NextAppointment
from .modeladmin_mixins import CrfModelAdmin


@admin.register(NextAppointment, site=intecomm_subject_admin)
class NextAppointmentAdmin(CrfModelAdmin):
    form = NextAppointmentForm
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Integrated Clinic",
            {"fields": ("health_facility", "appt_date", "info_source", "best_visit_code")},
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "info_source": admin.VERTICAL,
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "health_facility":
            kwargs["queryset"] = HealthFacility.on_site.filter(
                health_facility_type__name=INTEGRATED
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
