from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..models import HivReview
from .fieldsets import care_delivery_fieldset_tuple
from .modeladmin_mixins import CrfModelAdmin


@admin.register(HivReview, site=intecomm_subject_admin)
class HivReviewAdmin(CrfModelAdmin):
    # form = HivReviewForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        care_delivery_fieldset_tuple,
        (
            "Anit-retroviral therapy (ART)",
            {"fields": ("arv_initiated", "arv_initiation_actual_date")},
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "arv_initiated": admin.VERTICAL,
        "care_delivery": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
        "dx": admin.VERTICAL,
    }
