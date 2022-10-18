from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..models import HtnInitialReview
from .modeladmin_mixins import CrfModelAdmin


@admin.register(HtnInitialReview, site=intecomm_subject_admin)
class HtnInitialReviewAdmin(CrfModelAdmin):

    # form = HtnInitialReviewForm

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
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "managed_by": admin.VERTICAL,
    }
