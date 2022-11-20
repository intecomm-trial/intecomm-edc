from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..models import HivInitialReview
from .modeladmin_mixins import CrfModelAdmin


@admin.register(HivInitialReview, site=intecomm_subject_admin)
class HivInitialReviewAdmin(CrfModelAdmin):
    # form = HivInitialReviewForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Diagnosis and Care",
            {
                "fields": (
                    "dx_ago",
                    "dx_date",
                    "receives_care",
                    "clinic",
                    "clinic_other",
                )
            },
        ),
        (
            "Monitoring and Treatment",
            {
                "fields": (
                    "arv_initiated",
                    "arv_initiation_ago",
                    "arv_initiation_actual_date",
                    "has_vl",
                    "vl",
                    "vl_quantifier",
                    "vl_date",
                    "has_cd4",
                    "cd4",
                    "cd4_date",
                ),
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "arv_initiated": admin.VERTICAL,
        "clinic": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
        "has_cd4": admin.VERTICAL,
        "has_vl": admin.VERTICAL,
        "receives_care": admin.VERTICAL,
        "vl_quantifier": admin.VERTICAL,
    }

    def get_list_filter(self, request):
        list_filters = super().get_list_filter(request)
        list_filters = list(list_filters or [])
        list_filters.insert(4, "has_vl")
        return tuple(list_filters)
