from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset

from ..admin_site import intecomm_subject_admin
from ..forms import VitalsForm
from ..models import Vitals
from .modeladmin_mixins import CrfModelAdmin


@admin.register(Vitals, site=intecomm_subject_admin)
class VitalsAdmin(CrfModelAdmin):
    form = VitalsForm

    additional_instructions = "To be completed by the research nurse."

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Weight, Height and Temperature",
            {
                "fields": (
                    "weight_determination",
                    "weight",
                    "height",
                    "temperature",
                )
            },
        ),
        (
            "Blood Pressure: First reading",
            {
                "description": "Refer to SOP for blood pressure measurement procedure.",
                "fields": (
                    "bp_one_taken",
                    "bp_one_not_taken_reason",
                    "sys_blood_pressure_one",
                    "dia_blood_pressure_one",
                ),
            },
        ),
        (
            "Blood Pressure: Second reading",
            {
                "description": "Refer to SOP for blood pressure measurement procedure.",
                "fields": (
                    "bp_two_taken",
                    "bp_two_not_taken_reason",
                    "sys_blood_pressure_two",
                    "dia_blood_pressure_two",
                ),
            },
        ),
        (
            "Severe hypertension",
            {
                "description": "Refer to SOP on severe hypertension.",
                "fields": ("severe_htn",),
            },
        ),
        (
            "Comments",
            {
                "fields": ("comments",),
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "severe_htn": admin.VERTICAL,
        "weight_determination": admin.VERTICAL,
        "bp_one_taken": admin.VERTICAL,
        "bp_two_taken": admin.VERTICAL,
    }
