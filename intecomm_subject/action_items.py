from edc_action_item import Action, site_action_items
from edc_action_item.site_action_items import AlreadyRegistered
from edc_constants.constants import HIGH_PRIORITY
from edc_ltfu.constants import LTFU_ACTION

from .constants import MISSED_VISIT_ACTION


class MissedVisitAction(Action):
    name = MISSED_VISIT_ACTION
    priority = HIGH_PRIORITY
    display_name = "Missed Visits: LTFU"
    reference_model = "intecomm_subject.subjectvisitmissed"
    show_on_dashboard = True
    create_by_user = False

    def get_next_actions(self):
        ltfu = None
        if ltfu:
            next_actions = [LTFU_ACTION]
        return next_actions


def register_actions():
    try:
        site_action_items.register(MissedVisitAction)
    except AlreadyRegistered:
        pass


register_actions()
