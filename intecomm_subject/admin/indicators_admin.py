from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..models import Indicators
from .modeladmin_mixins import CrfModelAdmin


@admin.register(Indicators, site=intecomm_subject_admin)
class IndicatorsAdmin(CrfModelAdmin):
    # form = IndicatorsForm

    fieldsets = (
        (
            None,
            {
                "fields": ("subject_visit", "report_datetime"),
            },
        ),
        (
            "Weight, Height, Waist and Hip",
            {
                "description": "Provide if available",
                "fields": ("weight", "height", "waist", "hip"),
            },
        ),
        (
            "Blood Pressure: Reading 1",
            {
                "description": "Provide if available",
                "fields": (
                    "r1_taken",
                    "r1_reason_not_taken",
                    "sys_blood_pressure_r1",
                    "dia_blood_pressure_r1",
                ),
            },
        ),
        (
            "Blood Pressure: Reading 2",
            {
                "fields": (
                    "r2_taken",
                    "r2_reason_not_taken",
                    "sys_blood_pressure_r2",
                    "dia_blood_pressure_r2",
                )
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "r1_taken": admin.VERTICAL,
        "r2_taken": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
    }

    readonly_fields = []
