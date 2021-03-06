from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import intecomm_screening_admin
from ..forms import ScreeningPartTwoForm, get_part_one_fields
from ..models import ScreeningPartTwo
from .fieldsets import get_part_one_fieldset, get_part_two_fieldset
from .subject_screening_admin import SubjectScreeningAdmin


def get_fieldsets():
    return (
        get_part_one_fieldset(collapse=True),
        get_part_two_fieldset(),
        audit_fieldset_tuple,
    )


@admin.register(ScreeningPartTwo, site=intecomm_screening_admin)
class ScreeningPartTwoAdmin(SubjectScreeningAdmin):

    post_url_on_delete_name = "screening_dashboard_url"
    subject_listboard_url_name = "screening_listboard_url"

    form = ScreeningPartTwoForm

    fieldsets = get_fieldsets()

    readonly_fields = (*get_part_one_fields(),)
