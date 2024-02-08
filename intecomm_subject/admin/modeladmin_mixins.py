from __future__ import annotations

from django.contrib import admin
from django.utils.html import format_html
from django_audit_fields import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_crf.modeladmin_mixins import CrfStatusModelAdminMixin
from edc_model_admin.dashboard import ModelAdminCrfDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_model_admin.mixins import ModelAdminProtectPiiMixin
from edc_sites.admin import SiteModelAdminMixin

from intecomm_subject.choices import MISSED_PILLS

medication_adherence_description = """
<H5><B><font color="orange">Interviewer to read</font></B></H5>
<p>Drag the slider on the line below at
the point showing your best guess about how much medication
you have taken in the last month:<BR><BR>
<B>0%</B> means you have taken no medication<BR>
<B>50%</B> means you have taken half of your medication<BR>
<B>100%</B> means you have taken all your medication<BR>
</p>
"""


class CrfModelAdmin(
    ModelAdminProtectPiiMixin,  # must remain first
    SiteModelAdminMixin,
    CrfStatusModelAdminMixin,
    ModelAdminCrfDashboardMixin,
    SimpleHistoryAdmin,
):
    ordering = ("site__id", "report_datetime")


class MedicationAdherenceAdminMixin:
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Visual Score",
            {
                "description": format_html(medication_adherence_description),
                "fields": ("visual_score_slider", "visual_score_confirmed"),
            },
        ),
        (
            "Missed Medications",
            {
                "fields": (
                    "last_missed_pill",
                    "meds_missed_in_days",
                    "missed_pill_reason",
                    "other_missed_pill_reason",
                    "meds_shortage_in_days",
                    "meds_shortage_reason",
                    "meds_shortage_reason_other",
                )
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = ["missed_pill_reason", "meds_shortage_reason"]

    radio_fields = {
        "last_missed_pill": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
    }

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "last_missed_pill":
            kwargs["choices"] = MISSED_PILLS
        return super().formfield_for_choice_field(db_field, request, **kwargs)
