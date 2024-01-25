import re

import inflect
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_constants.constants import UUID_PATTERN
from edc_sites.admin import SiteModelAdminMixin

from intecomm_group.exceptions import PatientGroupNotRandomized
from intecomm_group.utils import get_assignment_description_for_patient_group

from ..admin_site import intecomm_screening_admin
from ..forms.patient_group_rando_form import PatientGroupRandoForm
from ..models import PatientGroupRando
from .modeladmin_mixins import BaseModelAdminMixin

p = inflect.engine()


@admin.register(PatientGroupRando, site=intecomm_screening_admin)
class PatientGroupRandoAdmin(SiteModelAdminMixin, BaseModelAdminMixin):
    form = PatientGroupRandoForm

    show_object_tools = True
    change_list_template: str = "intecomm_screening/admin/patientgroup_change_list.html"
    change_list_help = "Searches on encrypted data work on exact uppercase matches only"
    change_list_title = PatientGroupRando._meta.verbose_name_plural
    ordering = ("site__id", "randomized_datetime")

    fieldsets = (
        (None, {"fields": ["name"]}),
        (
            "Randomize",
            {
                "description": format_html(
                    "Complete this section when the group is COMPLETE and READY to "
                    "RANDOMIZE. <BR>"
                    "<B>Important: THIS STEP CANNOT BE UNDONE</B>"
                ),
                "fields": ("randomize_now", "confirm_randomize_now"),
            },
        ),
        (
            "Randomization",
            {
                "fields": ("group_identifier", "randomized", "randomized_datetime"),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "group_name",
        "arm",
        "group_id",
        "randomized_date",
        "user_created",
        "created",
    )

    list_filter = (
        "randomized",
        "report_datetime",
    )

    search_fields = (
        "name",
        "group_identifier",
    )

    radio_fields = {
        "randomize_now": admin.VERTICAL,
    }

    readonly_fields = ("group_identifier", "randomized_datetime", "randomized")

    @admin.display(description="Patient Group", ordering="name")
    def group_name(self, obj=None):
        return str(obj)

    @admin.display(description="Randomized", ordering="randomized_datetime")
    def randomized_date(self, obj=None):
        try:
            return obj.randomized_datetime.date()
        except AttributeError:
            return None

    @admin.display(description="Group identifier", ordering="group_identifier")
    def group_id(self, obj):
        return (
            None if re.match(UUID_PATTERN, str(obj.group_identifier)) else obj.group_identifier
        )

    @admin.display(description="Randomization")
    def arm(self, obj=None):
        try:
            arm_as_str = get_assignment_description_for_patient_group(obj.group_identifier)
        except PatientGroupNotRandomized:
            url = reverse(
                "intecomm_screening_admin:intecomm_screening_patientgroup_changelist"
            )
            url = f"{url}?q={obj.name}"
            link = format_html(
                f'<a title="Go to patient group" href="{url}">Edit Patient group</a>'
            )
        else:
            url = reverse("intecomm_group_admin:intecomm_group_patientgroup_changelist")
            url = f"{url}?q={obj.name}"
            link = format_html(
                f'<a title="Go to patient groups in followup" href="{url}">{arm_as_str}</a>'
            )
        return link

    def response_post_save_change(self, request, obj):
        url = reverse("intecomm_group_admin:intecomm_group_patientgroup_changelist")
        post_url = f"{url}?q={obj.name}"
        return HttpResponseRedirect(post_url)
