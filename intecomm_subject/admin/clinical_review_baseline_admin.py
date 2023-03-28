from django.contrib import admin
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_dx_review.fieldsets import get_clinical_review_baseline_cond_fieldset
from edc_dx_review.radio_fields import get_clinical_review_cond_radio_fields

from ..admin_site import intecomm_subject_admin
from ..forms import ClinicalReviewBaselineForm
from ..models import ClinicalReviewBaseline
from .modeladmin_mixins import CrfModelAdmin


@admin.register(ClinicalReviewBaseline, site=intecomm_subject_admin)
class ClinicalReviewBaselineAdmin(CrfModelAdmin):
    form = ClinicalReviewBaselineForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "HIV",
            {
                "description": format_html(
                    "<h5>Note for HIV(+) patients:</h5> If patient is HIV(+), estimate or "
                    "provide the date patient FIRST tested positive."
                ),
                "fields": get_clinical_review_baseline_cond_fieldset(cond="hiv")[1]["fields"],
            },
        ),
        get_clinical_review_baseline_cond_fieldset(cond="dm", title="Diabetes"),
        get_clinical_review_baseline_cond_fieldset(cond="htn", title="Hypertension"),
        ("Other", {"fields": ("health_insurance", "patient_club")}),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "health_insurance": admin.VERTICAL,
        "patient_club": admin.VERTICAL,
        **get_clinical_review_cond_radio_fields(),
    }
