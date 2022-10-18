from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..models import DmInitialReview
from .modeladmin_mixins import CrfModelAdmin


@admin.register(DmInitialReview, site=intecomm_subject_admin)
class DmInitialReviewAdmin(CrfModelAdmin):

    # form = DmInitialReviewForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Diagnosis and Treatment",
            {
                "fields": (
                    "dx_ago",
                    "dx_date",
                    "managed_by",
                    "med_start_ago",
                )
            },
        ),
        (
            "Fasting Blood Sugar Measurement",
            {
                "fields": (
                    "glucose_performed",
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
        "managed_by": admin.VERTICAL,
        "glucose_performed": admin.VERTICAL,
        "glucose_quantifier": admin.VERTICAL,
        "glucose_units": admin.VERTICAL,
        "glucose_fasting": admin.VERTICAL,
    }
