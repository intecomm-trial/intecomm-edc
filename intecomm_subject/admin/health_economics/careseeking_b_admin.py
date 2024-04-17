from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django_audit_fields import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ...admin_site import intecomm_subject_admin
from ...forms import CareseekingBForm
from ...models import CareseekingB
from ..modeladmin_mixins import CrfModelAdmin


@admin.register(CareseekingB, site=intecomm_subject_admin)
class CareseekingBAdmin(
    CrfModelAdmin,
):
    form = CareseekingBForm

    additional_instructions = render_to_string(
        "intecomm_subject/careseeking_b_instructions.html", context={}
    )

    fieldsets = (
        (
            _("Part B: INFORMATION ON ANY CARESEEKING IN THE PAST 3 MONTHS"),
            {"fields": ("subject_visit", "report_datetime")},
        ),
        (
            _("B1: Health visits in the past 3 months"),
            {
                "fields": (
                    "needed_care",
                    "accessed_care",
                    "no_accessed_care",
                    "no_accessed_care_other",
                    "care_facility",
                    "care_facility_other",
                    "care_type",
                    "outpatient_visits",
                )
            },
        ),
        (
            _("B2: Travel and expenses at last/most recent visit"),
            {
                "fields": (
                    "travel_method",
                    "travel_duration",
                    "travel_costs",
                    "food_costs",
                    "care_costs",
                )
            },
        ),
        (
            _("B3: Medications at last/most recent visit"),
            {
                "fields": (
                    "med_prescribed",
                    "med_conditions",
                    "med_conditions_other",
                    "med_collected",
                    "med_not_collected_reason",
                    "med_not_collected_reason_other",
                    "med_cost_tot",
                )
            },
        ),
        (
            _("B4: Tests at last/most recent visit"),
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
            _("B5: Time and expenses at last/most recent visit"),
            {
                "fields": (
                    "care_visit_duration",
                    "missed_activities",
                    "missed_activities_other",
                )
            },
        ),
        (
            _("B6: People who accompanied you to last/most recent visit"),
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
            _("B7: Your expenses in the past 3 months"),
            {
                "fields": (
                    "money_sources",
                    "money_sources_other",
                    "money_source_main",
                )
            },
        ),
        (
            _("B8: About your inpatient visit"),
            {
                "fields": (
                    "inpatient",
                    "inpatient_days",
                    "inpatient_reasons",
                    "inpatient_reasons_other",
                )
            },
        ),
        (
            _("B9: Inpatient visit: expenses"),
            {
                "description": _(
                    "Continue with this section if you were admitted "
                    "as an inpatient as indicated above"
                ),
                "fields": (
                    "inpatient_cost",
                    "inpatient_accompany",
                    "inpatient_food",
                    "inpatient_food_cost",
                    "inpatient_nowork_days",
                    "inpatient_household_nowork",
                    "inpatient_household_nowork_days",
                ),
            },
        ),
        (
            _("B10: Inpatient visit: sources of payment for expenses"),
            {
                "description": _(
                    "Continue with this section if you were admitted "
                    "as an inpatient as indicated above"
                ),
                "fields": (
                    "inpatient_money_sources",
                    "inpatient_money_sources_other",
                    "inpatient_money_sources_main",
                    "inpatient_money_sources_main_other",
                ),
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = [
        "travel_method",
        "med_conditions",
        "money_sources",
        "inpatient_reasons",
        "inpatient_money_sources",
    ]

    radio_fields = {
        "accompany": admin.VERTICAL,
        "accompany_alt": admin.VERTICAL,
        "accompany_wait": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
        "needed_care": admin.VERTICAL,
        "inpatient": admin.VERTICAL,
        "inpatient_accompany": admin.VERTICAL,
        "inpatient_food": admin.VERTICAL,
        "inpatient_household_nowork": admin.VERTICAL,
        "inpatient_money_sources_main": admin.VERTICAL,
        "med_collected": admin.VERTICAL,
        "med_not_collected_reason": admin.VERTICAL,
        "med_prescribed": admin.VERTICAL,
        "missed_activities": admin.VERTICAL,
        "money_source_main": admin.VERTICAL,
        "no_accessed_care": admin.VERTICAL,
        "accessed_care": admin.VERTICAL,
        "care_type": admin.VERTICAL,
        "care_facility": admin.VERTICAL,
        "tests_done": admin.VERTICAL,
        "tests_not_done_reason": admin.VERTICAL,
        "tests_requested": admin.VERTICAL,
    }
