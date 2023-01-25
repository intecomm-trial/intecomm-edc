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

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Weight, Height, Waist and Hip",
            {
                "fields": (
                    "weight",
                    "weight_determination",
                    "height",
                    "waist",
                    "hip",
                )
            },
        ),
        (
            "Blood Pressure",
            {
                "description": (
                    "To be completed by the research nurse. <BR>"
                    "Refer to SOP for blood pressure measurement procedure."
                ),
                "fields": (
                    "sys_blood_pressure_one",
                    "dia_blood_pressure_one",
                    "sys_blood_pressure_two",
                    "dia_blood_pressure_two",
                    "severe_htn",
                ),
            },
        ),
        (
            "Heart Rate, Respiratory Rate and Temperature",
            {
                "fields": (
                    "heart_rate",
                    "respiratory_rate",
                    "temperature",
                ),
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "severe_htn": admin.VERTICAL,
    }
