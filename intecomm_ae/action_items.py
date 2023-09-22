from __future__ import annotations

from typing import TYPE_CHECKING

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from edc_action_item import ActionWithNotification, site_action_items
from edc_adverse_event.action_items import HospitalizationAction
from edc_adverse_event.constants import (
    AE_FOLLOWUP_ACTION,
    AE_INITIAL_ACTION,
    DEATH_REPORT_ACTION,
)
from edc_constants.constants import DEAD, HIGH_PRIORITY, YES
from edc_ltfu.constants import LOST_TO_FOLLOWUP
from edc_notification.utils import get_email_contacts
from edc_reportable import GRADE5
from edc_visit_schedule.utils import get_offschedule_models
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM

from intecomm_group.utils import get_assignment_for_patient_group
from intecomm_prn.constants import OFFSCHEDULE_COMM_ACTION, OFFSCHEDULE_INTE_ACTION

if TYPE_CHECKING:
    from intecomm_prn.models import OffScheduleComm, OffScheduleInte


class AeFollowupAction(ActionWithNotification):
    name = AE_FOLLOWUP_ACTION
    display_name = "Submit AE Followup Report"
    notification_display_name = "AE Followup Report"
    parent_action_names = [AE_INITIAL_ACTION, AE_FOLLOWUP_ACTION]
    reference_model = "intecomm_ae.aefollowup"
    related_reference_model = "intecomm_ae.aeinitial"
    related_reference_fk_attr = "ae_initial"
    create_by_user = False
    show_link_to_changelist = True
    admin_site_name = "intecomm_ae_admin"
    instructions = mark_safe(  # nosec B308, B703
        "Upon submission the TMG group will be notified "
        f'by email at <a href="mailto:{get_email_contacts("tmg") or "#"}">'
        f'{get_email_contacts("tmg") or "unknown"}</a>'
    )
    priority = HIGH_PRIORITY

    def get_next_actions(self):
        next_actions = []

        # add AE followup to next_actions if followup.
        next_actions = self.append_to_next_if_required(
            next_actions=next_actions,
            action_name=self.name,
            required=self.reference_obj.followup == YES,
        )

        # add Death Report to next_actions if G5/Death
        next_actions = self.append_to_next_if_required(
            next_actions=next_actions,
            action_name=DEATH_REPORT_ACTION,
            required=(
                self.reference_obj.outcome == DEAD or self.reference_obj.ae_grade == GRADE5
            ),
        )

        # add Study termination to next_actions if LTFU
        if self.reference_obj.outcome == LOST_TO_FOLLOWUP:
            for offschedule_model in get_offschedule_models(
                subject_identifier=self.subject_identifier,
                report_datetime=self.reference_obj.report_datetime,
            ):
                action_cls = site_action_items.get_by_model(model=offschedule_model)
                next_actions = self.append_to_next_if_required(
                    next_actions=next_actions,
                    action_name=action_cls.name,
                    required=True,
                )
        return next_actions


class AeInitialAction(ActionWithNotification):
    name = AE_INITIAL_ACTION
    display_name = "Submit AE Initial Report"
    notification_display_name = "AE Initial Report"
    reference_model = "intecomm_ae.aeinitial"
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = "intecomm_ae_admin"
    instructions = "Complete the initial AE report"
    priority = HIGH_PRIORITY

    def get_next_actions(self):
        """Returns next actions.

        1. Add death report action if death
        """
        next_actions = []
        deceased = self.reference_obj.ae_grade == GRADE5
        # add next AeFollowup if not deceased
        if not deceased:
            next_actions = self.append_to_next_if_required(
                action_name=AE_FOLLOWUP_ACTION, next_actions=next_actions
            )
        # add next Death report if G5/Death
        next_actions = self.append_to_next_if_required(
            next_actions=next_actions,
            action_name=DEATH_REPORT_ACTION,
            required=deceased,
        )
        return next_actions


class DeathReportAction(ActionWithNotification):
    name = DEATH_REPORT_ACTION
    display_name = "Submit Death Report"
    notification_display_name = "Death Report"
    reference_model = "intecomm_ae.deathreport"
    parent_action_names = [AE_INITIAL_ACTION, AE_FOLLOWUP_ACTION]
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = "intecomm_ae_admin"
    priority = HIGH_PRIORITY
    singleton = True
    dirty_fields = ["cause_of_death"]

    def get_next_actions(self):
        next_actions = []
        try:
            self.off_schedule_cls.objects.get(subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            if self.assignment == COMMUNITY_ARM:
                next_actions.extend([OFFSCHEDULE_COMM_ACTION])
            elif self.assignment == FACILITY_ARM:
                next_actions.extend([OFFSCHEDULE_INTE_ACTION])
        return next_actions

    @property
    def group_identifier(self) -> str:
        return (
            django_apps.get_model("intecomm_screening.patientlog")
            .objects.get(subject_identifier=self.subject_identifier)
            .group_identifier
        )

    @property
    def assignment(self) -> str:
        return get_assignment_for_patient_group(self.group_identifier)

    @property
    def off_schedule_cls(self) -> OffScheduleComm | OffScheduleInte:
        if self.assignment == COMMUNITY_ARM:
            return django_apps.get_model("intecomm_prn.offschedulecomm")
        elif self.assignment == FACILITY_ARM:
            return django_apps.get_model("intecomm_prn.offscheduleinte")


class HospitalizationAction(HospitalizationAction):
    reference_model = "intecomm_ae.hospitalization"
    admin_site_name = "intecomm_ae_admin"


site_action_items.register(AeFollowupAction)
site_action_items.register(AeInitialAction)
site_action_items.register(DeathReportAction)
site_action_items.register(HospitalizationAction)
