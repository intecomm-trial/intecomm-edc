from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_dx import get_diagnosis_labels_prefixes
from edc_dx_review.fieldsets import get_clinical_review_cond_fieldsets
from edc_dx_review.radio_fields import get_clinical_review_cond_radio_fields

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
        *get_clinical_review_cond_fieldsets(),
        ("Complications", {"fields": ("complications",)}),
        treatment_pay_methods_fieldset_tuple,
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "complications": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
        "health_insurance": admin.VERTICAL,
        "patient_club": admin.VERTICAL,
        **get_clinical_review_cond_radio_fields(),
    }

    filter_horizontal = [f"{cond}_reason" for cond in get_diagnosis_labels_prefixes()]
