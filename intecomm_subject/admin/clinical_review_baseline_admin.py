from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_dx_review.fieldsets import get_clinical_review_baseline_cond_fieldsets
from edc_dx_review.radio_fields import get_clinical_review_cond_radio_fields

from ..admin_site import intecomm_subject_admin
from ..forms.clinical_review_baseline_form import ClinicalReviewBaselineForm
from ..models import ClinicalReviewBaseline
from .modeladmin_mixins import CrfModelAdmin


@admin.register(ClinicalReviewBaseline, site=intecomm_subject_admin)
class ClinicalReviewBaselineAdmin(CrfModelAdmin):

    form = ClinicalReviewBaselineForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        *get_clinical_review_baseline_cond_fieldsets(),
        ("Complications", {"fields": ("complications",)}),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "complications": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
    }
    radio_fields |= get_clinical_review_cond_radio_fields()
