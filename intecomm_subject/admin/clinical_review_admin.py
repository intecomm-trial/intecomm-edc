from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..forms import ClinicalReviewForm
from ..models import ClinicalReview
from .fieldsets import treatment_pay_methods_fieldset_tuple
from .modeladmin_mixins import CrfModelAdmin


@admin.register(ClinicalReview, site=intecomm_subject_admin)
class ClinicalReviewAdmin(CrfModelAdmin):
    form = ClinicalReviewForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "HYPERTENSION",
            {
                "fields": (
                    "htn_test",
                    "htn_test_date",
                    "htn_reason",
                    "htn_reason_other",
                    "htn_dx",
                )
            },
        ),
        (
            "DIABETES",
            {
                "fields": (
                    "dm_test",
                    "dm_test_date",
                    "dm_reason",
                    "dm_reason_other",
                    "dm_dx",
                )
            },
        ),
        (
            "HIV",
            {
                "fields": (
                    "hiv_test",
                    "hiv_test_date",
                    "hiv_reason",
                    "hiv_reason_other",
                    "hiv_dx",
                )
            },
        ),
        ("Complications", {"fields": ("complications",)}),
        treatment_pay_methods_fieldset_tuple,
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "htn_test": admin.VERTICAL,
        "dm_test": admin.VERTICAL,
        "health_insurance": admin.VERTICAL,
        "hiv_test": admin.VERTICAL,
        "htn_dx": admin.VERTICAL,
        "dm_dx": admin.VERTICAL,
        "hiv_dx": admin.VERTICAL,
        "complications": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
        "patient_club": admin.VERTICAL,
    }

    filter_horizontal = [
        "htn_reason",
        "dm_reason",
        "hiv_reason",
    ]
