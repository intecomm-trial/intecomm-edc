from edc_action_item.action_with_notification import ActionWithNotification
from edc_action_item.site_action_items import site_action_items
from edc_adverse_event.constants import DEATH_REPORT_ACTION
from edc_constants.constants import HIGH_PRIORITY
from edc_ltfu.constants import LTFU_ACTION
from edc_offstudy.constants import END_OF_STUDY_ACTION
from edc_protocol_incident.action_items import (
    ProtocolIncidentAction as BaseProtocolIncidentAction,
)
from edc_transfer.action_items import SubjectTransferAction as BaseSubjectTransferAction
from edc_visit_schedule.constants import OFFSCHEDULE_ACTION

from intecomm_subject.constants import MISSED_VISIT_ACTION


class OffscheduleAction(ActionWithNotification):
    name = OFFSCHEDULE_ACTION
    display_name = "Submit Off-Schedule (followup)"
    notification_display_name = "Off-Schedule (followup)"
    parent_action_names = [
        DEATH_REPORT_ACTION,
        LTFU_ACTION,
    ]
    reference_model = "intecomm_prn.offschedulefollowup"
    show_link_to_changelist = True
    admin_site_name = "intecomm_prn_admin"
    priority = HIGH_PRIORITY
    singleton = True


class EndOfStudyAction(ActionWithNotification):
    name = END_OF_STUDY_ACTION
    display_name = "Submit End of Study Report"
    notification_display_name = "End of Study Report"
    parent_action_names = [OFFSCHEDULE_ACTION]
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


class ProtocolIncidentAction(BaseProtocolIncidentAction):
    reference_model = "intecomm_prn.protocolincident"
    admin_site_name = "intecomm_prn_admin"


site_action_items.register(EndOfStudyAction)
site_action_items.register(LossToFollowupAction)
site_action_items.register(OffscheduleAction)
site_action_items.register(ProtocolIncidentAction)
site_action_items.register(SubjectTransferAction)
