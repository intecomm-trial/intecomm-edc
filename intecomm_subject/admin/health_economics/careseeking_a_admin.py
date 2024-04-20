from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django_audit_fields import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ...admin_site import intecomm_subject_admin
from ...forms import CareseekingAForm
from ...models import CareseekingA
from ..modeladmin_mixins import CrfModelAdmin


@admin.register(CareseekingA, site=intecomm_subject_admin)
class CareseekingAAdmin(
    CrfModelAdmin,
):
    form = CareseekingAForm

    additional_instructions = render_to_string(
        "intecomm_subject/careseeking_a_instructions.html", context={}
    )

    fieldsets = (
        (
            _("PART A: INFORMATION ON TODAY’S VISIT"),
            {"fields": ("subject_visit", "report_datetime")},
        ),
        (
            _("A1: Travel, expenses and reason for today's visit"),
            {
                "fields": (
                    "travel_method",
                    "travel_duration",
                    "travel_cost",
                    "food_cost",
                    "care_visit_reason",
                    "care_visit_reason_other",
                    "care_visit_cost",
                )
            },
        ),
        (
            _("A3: Medication costs for today's visit"),
            {
                "fields": (
                    "med_prescribed",
                    "med_conditions",
                    "med_conditions_other",
                    "med_collected",
                    "med_not_collected_reason",
                    "med_not_collected_reason_other",
                    "med_cost_tot",
                    "med_cost_hiv",
                    "med_cost_htn",
                    "med_cost_dm",
                    "med_cost_other",
                    "med_collected_location",
                    "med_collected_location_other",
                )
            },
        ),
        (
            _("A4: Diagnostic costs for today's visit"),
            {
                "fields": (
                    "tests_requested",
                    "tests_done",
                    "tests_not_done_reason",
                    "tests_not_done_other",
                    "tests_cost",
                )
            },
        ),
        (
            _("A5: Time for today's visit"),
            {
                "fields": (
                    "care_visit_duration",
                    "with_hcw_duration",
                    "missed_activities",
                    "missed_activities_other",
                )
            },
        ),
        (
            _("A6: Referral from today's visit"),
            {
                "fields": (
                    "referral",
                    "referral_type",
                    "referral_facility",
                )
            },
        ),
        (
            _("A7: People who accompanied you to today's visit"),
            {
                "fields": (
                    "accompany",
                    "accompany_num",
                    "accompany_wait",
                    "accompany_alt",
                    "accompany_alt_other",
                )
            },
        ),
        (
            _("A8: Your expenses for today's visit"),
            {
                "fields": (
                    "money_sources",
                    "money_sources_other",
                    "money_source_main",
                )
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = [
        "travel_method",
        "care_visit_reason",
        "med_conditions",
        "money_sources",
    ]

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "med_prescribed": admin.VERTICAL,
        "med_collected": admin.VERTICAL,
        "med_not_collected_reason": admin.VERTICAL,
        "tests_requested": admin.VERTICAL,
        "tests_done": admin.VERTICAL,
        "tests_not_done_reason": admin.VERTICAL,
        "missed_activities": admin.VERTICAL,
        "referral": admin.VERTICAL,
        "referral_type": admin.VERTICAL,
        "referral_facility": admin.VERTICAL,
        "money_source_main": admin.VERTICAL,
        "accompany": admin.VERTICAL,
        "accompany_wait": admin.VERTICAL,
        "accompany_alt": admin.VERTICAL,
        "med_collected_location": admin.VERTICAL,
    }
