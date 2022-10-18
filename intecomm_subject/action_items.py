from edc_action_item import site_action_items
from edc_action_item.site_action_items import AlreadyRegistered
from edc_visit_tracking.action_items import MissedVisitAction as BaseMissedVisitAction


class MissedVisitAction(BaseMissedVisitAction):
    reference_model = "intecomm_subject.subjectvisitmissed"
    admin_site_name: str = "intecomm_subject_admin"


def register_actions():
    try:
        site_action_items.register(MissedVisitAction)
    except AlreadyRegistered:
        pass


register_actions()
