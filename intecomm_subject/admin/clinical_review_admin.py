from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_dx import get_diagnosis_labels_prefixes
from edc_dx_review.fieldsets import get_clinical_review_cond_fieldsets
from edc_dx_review.radio_fields import get_clinical_review_cond_radio_fields

from ..admin_site import intecomm_subject_admin
from ..forms import ClinicalReviewForm
from ..models import ClinicalReview
from .modeladmin_mixins import CrfModelAdmin


@admin.register(ClinicalReview, site=intecomm_subject_admin)
class ClinicalReviewAdmin(CrfModelAdmin):
    form = ClinicalReviewForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        *get_clinical_review_cond_fieldsets(),
        ("Complications", {"fields": ("complications",)}),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "complications": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
    }
    radio_fields |= get_clinical_review_cond_radio_fields()

    filter_horizontal = [f"{cond.lower()}_reason" for cond in get_diagnosis_labels_prefixes()]
