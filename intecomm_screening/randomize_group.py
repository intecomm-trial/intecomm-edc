from edc_constants.constants import COMPLETE
from edc_utils import get_utcnow


class GroupAlreadyRandomized(Exception):
    pass


class GroupRandomizationError(Exception):
    pass


def randomize_group(instance):
    if instance.randomized:
        raise GroupAlreadyRandomized(f"Group is already randomized. Got {instance}.")
    if instance.status != COMPLETE:
        raise GroupRandomizationError(f"Group is not complete. Got {instance}.")
    return True, get_utcnow(), instance.user_modified
