from edc_action_item import ActionWithNotification, site_action_items
from edc_action_item.site_action_items import AlreadyRegistered

from .constants import RANDOMIZATION_ACTION


class RandomizationAction(ActionWithNotification):
    name = RANDOMIZATION_ACTION
    display_name = "Group randomisation notification"
    notification_display_name = "Group randomisation notification"
    reference_model = "intecomm_subject.patientgroup"
    admin_site_name: str = "intecomm_subject_admin"
    notify_on_new_and_no_reference_obj = False
    notify_on_close = True
    create_by_user = False
    show_link_to_changelist = True

    def close_action_item_on_save(self):
        return True

    def create_next_action_items(self):
        pass


def register_actions():
    try:
        site_action_items.register(RandomizationAction)
    except AlreadyRegistered:
        pass


register_actions()
