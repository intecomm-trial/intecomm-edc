from django.contrib import admin
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

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
                "fields": ("hiv_test", "hiv_test_ago", "hiv_test_date", "hiv_dx"),
            },
        ),
        ("Diabetes", {"fields": ("dm_test", "dm_test_ago", "dm_test_date", "dm_dx")}),
        (
            "Hypertension",
            {"fields": ("htn_test", "htn_test_ago", "htn_test_date", "htn_dx")},
        ),
        ("Other", {"fields": ("health_insurance", "patient_club")}),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "dm_dx": admin.VERTICAL,
        "dm_test": admin.VERTICAL,
        "health_insurance": admin.VERTICAL,
        "hiv_dx": admin.VERTICAL,
        "hiv_test": admin.VERTICAL,
        "htn_dx": admin.VERTICAL,
        "htn_test": admin.VERTICAL,
        "patient_club": admin.VERTICAL,
    }
