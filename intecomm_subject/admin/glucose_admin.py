from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..models import Glucose
from .modeladmin_mixins import CrfModelAdmin


@admin.register(Glucose, site=intecomm_subject_admin)
class GlucoseAdmin(CrfModelAdmin):
    # form = GlucoseForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Blood Sugar Measurement",
            {
                "fields": (
                    "glucose_fasting",
                    "glucose_fasting_duration_str",
                    "glucose_date",
                    "glucose_value",
                    "glucose_quantifier",
                    "glucose_units",
                ),
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "glucose_units": admin.VERTICAL,
        "glucose_fasting": admin.VERTICAL,
        "glucose_quantifier": admin.VERTICAL,
    }
