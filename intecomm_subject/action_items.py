from edc_action_item import site_action_items
from edc_action_item.site_action_items import AlreadyRegistered
from edc_visit_tracking.action_items import MissedVisitAction as BaseMissedVisitAction


# TODO: review if this is needed
class MissedVisitAction(BaseMissedVisitAction):
    reference_model = "intecomm_subject.subjectvisitmissed"
    admin_site_name: str = "intecomm_subject_admin"
    show_on_dashboard = False

    def is_ltfu(self) -> bool:
        return False


def register_actions():
    try:
        site_action_items.register(MissedVisitAction)
    except AlreadyRegistered:
        pass


register_actions()
