from edc_action_item.action_with_notification import ActionWithNotification
from edc_action_item.exceptions import ActionError
from edc_action_item.site_action_items import site_action_items
from edc_adverse_event.constants import DEATH_REPORT_ACTION
from edc_constants.constants import HIGH_PRIORITY
from edc_locator.action_items import SubjectLocatorAction as BaseSubjectLocatorAction
from edc_ltfu.constants import LTFU_ACTION
from edc_offstudy.constants import END_OF_STUDY_ACTION
from edc_protocol_incident.action_items import (
    ProtocolIncidentAction as BaseProtocolIncidentAction,
)
from edc_transfer.action_items import SubjectTransferAction as BaseSubjectTransferAction
from edc_transfer.constants import SUBJECT_TRANSFER_ACTION
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM

from intecomm_group.utils import get_assignment_for_patient_group
from intecomm_screening.models import PatientLog
from intecomm_subject.constants import MISSED_VISIT_ACTION

from .constants import OFFSCHEDULE_COMM_ACTION, OFFSCHEDULE_INTE_ACTION

site_action_items.unregister(BaseSubjectLocatorAction)


class SubjectLocatorAction(BaseSubjectLocatorAction):
    reference_model = "intecomm_prn.subjectlocator"
    admin_site_name = "intecomm_prn_admin"


# TODO: action item for end of study does not show
class OffscheduleInteAction(ActionWithNotification):
    name = OFFSCHEDULE_INTE_ACTION
    display_name = "Submit Off-Schedule (Facility)"
    notification_display_name = "Off-Schedule (Facility)"
    parent_action_names = [
        DEATH_REPORT_ACTION,
        LTFU_ACTION,
        SUBJECT_TRANSFER_ACTION,
    ]
    reference_model = "intecomm_prn.offscheduleinte"
    show_link_to_changelist = True
    admin_site_name = "intecomm_prn_admin"
    priority = HIGH_PRIORITY
    singleton = True
    next_actions = [END_OF_STUDY_ACTION]


class OffscheduleCommAction(ActionWithNotification):
    name = OFFSCHEDULE_COMM_ACTION
    display_name = "Submit Off-Schedule (Community)"
    notification_display_name = "Off-Schedule (Community)"
    parent_action_names = [
        DEATH_REPORT_ACTION,
        LTFU_ACTION,
        SUBJECT_TRANSFER_ACTION,
    ]
    reference_model = "intecomm_prn.offschedulecomm"
    show_link_to_changelist = True
    admin_site_name = "intecomm_prn_admin"
    priority = HIGH_PRIORITY
    singleton = True
    next_actions = [END_OF_STUDY_ACTION]


class EndOfStudyAction(ActionWithNotification):
    name = END_OF_STUDY_ACTION
    display_name = "Submit End of Study Report"
    notification_display_name = "End of Study Report"
    parent_action_names = [OFFSCHEDULE_INTE_ACTION, OFFSCHEDULE_COMM_ACTION]
    reference_model = "intecomm_prn.endofstudy"
    show_link_to_changelist = True
    admin_site_name = "intecomm_prn_admin"
    priority = HIGH_PRIORITY
    singleton = True


class LossToFollowupAction(ActionWithNotification):
    name = LTFU_ACTION
    display_name = "Submit Loss to Follow Up Report"
    notification_display_name = " Loss to Follow Up Report"
    parent_action_names = [MISSED_VISIT_ACTION]
    reference_model = "intecomm_prn.losstofollowup"
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = "intecomm_prn_admin"
    priority = HIGH_PRIORITY
    singleton = True


class SubjectTransferAction(BaseSubjectTransferAction):
    reference_model = "intecomm_prn.subjecttransfer"
    admin_site_name = "intecomm_prn_admin"

    def get_next_actions(self):
        patient_log = PatientLog.objects.get(
            subject_identifier=self.reference_obj.subject_identifier
        )
        assignment = get_assignment_for_patient_group(
            patient_log.group_identifier,
        )
        if assignment == COMMUNITY_ARM:
            next_actions = [OFFSCHEDULE_COMM_ACTION]
        elif assignment == FACILITY_ARM:
            next_actions = [OFFSCHEDULE_INTE_ACTION]
        else:
            raise ActionError(
                f"Unable to determine assignment. Got {self.reference_obj.subject_identifier}"
            )
        return next_actions


class ProtocolIncidentAction(BaseProtocolIncidentAction):
    reference_model = "intecomm_prn.protocolincident"
    admin_site_name = "intecomm_prn_admin"


site_action_items.register(EndOfStudyAction)
site_action_items.register(LossToFollowupAction)
site_action_items.register(OffscheduleInteAction)
site_action_items.register(OffscheduleCommAction)
site_action_items.register(ProtocolIncidentAction)
site_action_items.register(SubjectTransferAction)
site_action_items.register(SubjectLocatorAction)
