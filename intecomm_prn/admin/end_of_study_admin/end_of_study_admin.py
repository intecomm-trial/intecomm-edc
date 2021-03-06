from django.contrib import admin
from edc_action_item import action_fieldset_tuple
from edc_data_manager.data_manager_modeladmin_mixin import DataManagerModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin, audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ...admin_site import intecomm_prn_admin
from ...forms import EndOfStudyPhaseThreeForm
from ...models import EndOfStudy
from .model_admin_mixin import EndOfStudyAdminMixin


class EndOfStudyAdmin(
    EndOfStudyAdminMixin,
    DataManagerModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):

    form = EndOfStudyPhaseThreeForm

    fieldsets = (
        [
            "Part 1:",
            {
                "fields": (
                    "subject_identifier",
                    "offschedule_datetime",
                    "last_seen_date",
                    "offschedule_reason",
                    "other_offschedule_reason",
                    "ltfu_date",
                    "death_date",
                    "clinical_withdrawal_reason",
                    "clinical_withdrawal_reason_other",
                    "toxicity_withdrawal_reason",
                    "toxicity_withdrawal_reason_other",
                    "comment",
                )
            },
        ],
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "offschedule_reason": admin.VERTICAL,
        "clinical_withdrawal_reason": admin.VERTICAL,
        "toxicity_withdrawal_reason": admin.VERTICAL,
    }


intecomm_prn_admin.register(EndOfStudy, EndOfStudyAdmin)
