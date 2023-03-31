from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..forms import ComplicationsBaselineForm
from ..models import ComplicationsBaseline
from .modeladmin_mixins import CrfModelAdmin


@admin.register(ComplicationsBaseline, site=intecomm_subject_admin)
class ComplicationsBaselineAdmin(CrfModelAdmin):
    form = ComplicationsBaselineForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Complications",
            {
                "fields": (
                    "stroke",
                    "stroke_ago",
                    "heart_attack",
                    "heart_attack_ago",
                    "renal_disease",
                    "renal_disease_ago",
                    "vision",
                    "vision_ago",
                    "numbness",
                    "numbness_ago",
                    "foot_ulcers",
                    "foot_ulcers_ago",
                    "complications",
                    "complications_other",
                )
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "heart_attack": admin.VERTICAL,
        "stroke": admin.VERTICAL,
        "renal_disease": admin.VERTICAL,
        "vision": admin.VERTICAL,
        "numbness": admin.VERTICAL,
        "foot_ulcers": admin.VERTICAL,
        "complications": admin.VERTICAL,
    }
