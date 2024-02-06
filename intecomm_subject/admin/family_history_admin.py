from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..forms import FamilyHistoryForm
from ..models import FamilyHistory
from .modeladmin_mixins import CrfModelAdmin


@admin.register(FamilyHistory, site=intecomm_subject_admin)
class FamilyHistoryAdmin(CrfModelAdmin):
    form = FamilyHistoryForm
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Part 1",
            {"fields": ("htn_in_household", "dm_in_household", "hiv_in_household")},
        ),
        (
            "Part 2",
            {
                "fields": (
                    "high_bp_bs_tf",
                    "overweight_tf",
                    "salty_foods_tf",
                    "excercise_tf",
                    "take_medicine_tf",
                    "stop_htn_meds_tf",
                    "traditional_htn_tf",
                    "stop_dm_meds_tf",
                    "traditional_dm_tf",
                    "dm_cause_tf",
                )
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "htn_in_household": admin.VERTICAL,
        "dm_in_household": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
        "hiv_in_household": admin.VERTICAL,
        "high_bp_bs_tf": admin.VERTICAL,
        "overweight_tf": admin.VERTICAL,
        "salty_foods_tf": admin.VERTICAL,
        "excercise_tf": admin.VERTICAL,
        "take_medicine_tf": admin.VERTICAL,
        "stop_htn_meds_tf": admin.VERTICAL,
        "traditional_htn_tf": admin.VERTICAL,
        "stop_dm_meds_tf": admin.VERTICAL,
        "traditional_dm_tf": admin.VERTICAL,
        "dm_cause_tf": admin.VERTICAL,
    }
