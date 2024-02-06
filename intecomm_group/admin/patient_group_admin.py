import re

import inflect
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_audit_fields.admin import audit_fieldset_tuple
from edc_constants.constants import COMPLETE, NEW, NOT_APPLICABLE, UUID_PATTERN
from edc_model_admin.mixins import ModelAdminRedirectAllToChangelistMixin
from edc_sites.admin import SiteModelAdminMixin
from intecomm_form_validators import RECRUITING
from intecomm_rando.constants import COMMUNITY_ARM

from intecomm_screening.admin.modeladmin_mixins import BaseModelAdminMixin

from ..admin_site import intecomm_group_admin
from ..exceptions import PatientGroupNotRandomized
from ..forms import PatientGroupForm
from ..models import PatientGroup
from ..utils import (
    get_assignment_description_for_patient_group,
    get_group_subject_dashboards_url,
)

p = inflect.engine()


@admin.register(PatientGroup, site=intecomm_group_admin)
class PatientGroupAdmin(
    SiteModelAdminMixin, ModelAdminRedirectAllToChangelistMixin, BaseModelAdminMixin
):
    """Modeladmin for patient groups in follow-up or dissolved.

    See `get_queryset`"""

    form = PatientGroupForm

    show_object_tools = True
    change_list_template: str = "intecomm_group/admin/patientgroup_change_list.html"
    show_save_next = False
    show_cancel = True

    changelist_url = "intecomm_group_admin:intecomm_group_patientgroup_changelist"
    change_search_field_name = "group_identifier"
    add_search_field_name = "group_identifier"

    fieldsets = (
        (
            None,
            {"fields": ("report_datetime", "name", "status", "notes")},
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "__str__",
        "to_subjects",
        "arm",
        "meetings",
        "group_id",
        "randomized_date",
        "opened",
        "user_created",
        "created",
    )

    list_filter = (
        "status",
        "randomized",
        "report_datetime",
        "randomized_datetime",
    )

    search_fields = (
        "name",
        "group_identifier",
        "patients__legal_name__exact",
        "patients__familiar_name__exact",
        "patients__initials__iexact",
    )

    radio_fields = {
        "status": admin.VERTICAL,
    }

    readonly_fields = (
        "report_datetime",
        "name",
        "status",
        "randomized",
        "randomized_datetime",
    )

    @admin.display(description="Randomized", ordering="randomized_datetime")
    def randomized_date(self, obj=None):
        try:
            return obj.randomized_datetime.date()
        except AttributeError:
            return None

    @admin.display(description="Status", ordering="status")
    def group_status(self, obj):
        return format_html(f'<span class="nowrap">{obj.get_status_display()}</span>')

    @admin.display(description="Group identifier", ordering="group_identifier")
    def group_id(self, obj):
        return (
            None if re.match(UUID_PATTERN, str(obj.group_identifier)) else obj.group_identifier
        )

    @admin.display(description="Opened", ordering="report_datetime")
    def opened(self, obj=None):
        return obj.report_datetime.date()

    @admin.display(description="Randomization")
    def arm(self, obj=None):
        try:
            arm_as_str = get_assignment_description_for_patient_group(obj.group_identifier)
        except PatientGroupNotRandomized:
            link = None
        else:
            url = reverse(
                "intecomm_screening_admin:intecomm_screening_patientgroup_changelist"
            )
            url = f"{url}?q={obj.name}"
            link = format_html(
                f'<a title="Back to ALL patient groups" href="{url}">{arm_as_str}</a>'
            )
        return link

    @admin.display(description="Meetings")
    def meetings(self, obj=None) -> str:
        url = NOT_APPLICABLE
        try:
            arm_as_str = get_assignment_description_for_patient_group(obj.group_identifier)
        except PatientGroupNotRandomized:
            pass
        else:
            if arm_as_str == COMMUNITY_ARM:
                name = "+".join(obj.name.split(" "))
                url = reverse(
                    "intecomm_group_admin:intecomm_group_patientgroupmeeting_changelist"
                )
                url = f"{url}?q={name}"
                url = format_html(f'<a href="{url}">Meetings</a>')
        return url

    @admin.display(description="Dashboards")
    def to_subjects(self, obj=None):
        cnt = obj.patients.all().count()
        url = get_group_subject_dashboards_url(obj)
        title = _("Go to subject dashboards")
        return format_html(
            f'<a title="{title}" href="{url}">'
            f'<span class="nowrap">{cnt}&nbsp;{p.plural("subject", cnt)}</span></a>'
        )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .exclude(status__in=[NEW, RECRUITING, COMPLETE], randomized=False)
        )
