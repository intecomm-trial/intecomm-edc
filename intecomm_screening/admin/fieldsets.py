from django.utils.safestring import mark_safe

from ..forms import get_part_one_fields, get_part_two_fields


def get_part_one_fieldset(collapse=None):

    dct = {
        "description": mark_safe(
            "To be completed by the <u>study clinician</u> or the "
            "<u>research nurse</u> in consultation with the study clinician"
        ),
        "fields": get_part_one_fields(),
    }
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 1", dct


def get_part_two_fieldset(collapse=None):
    dct = {
        "description": mark_safe(
            "To be completed by the <u>study clinician</u> or the "
            "<u>research nurse</u> in consultation with the study clinician"
        ),
        "fields": get_part_two_fields(),
    }
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 2", dct
