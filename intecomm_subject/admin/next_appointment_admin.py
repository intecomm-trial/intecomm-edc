from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import intecomm_subject_admin
from ..forms import NextAppointmentForm
from ..models import NextAppointment
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(NextAppointment, site=intecomm_subject_admin)
class NextAppointmentAdmin(CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin):
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
        # "best_visit_code": admin.VERTICAL,
    }
