from typing import Tuple

from django.utils.html import format_html
from django_audit_fields import audit_fieldset_tuple
from edc_action_item import ActionItemModelAdminMixin, action_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..models import EndOfStudy


class OffScheduleAdmin(
    SiteModelAdminMixin,
    ActionItemModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = None

    additional_instructions = format_html(
        "{}",
        '<span style="color:orange;font-weight:bold">Note:</span> Detailed '
        "information about study termination will be asked for on the "
        f"<b>{EndOfStudy._meta.verbose_name}</b> form",
    )

    fieldsets = (
        (None, {"fields": ("subject_identifier", "offschedule_datetime")}),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    def get_list_display(self, request) -> Tuple[str, ...]:
        list_display = super().get_list_display(request)
        custom_fields = ("subject_identifier", "dashboard", "offschedule_datetime")
        return custom_fields + tuple(f for f in list_display if f not in custom_fields)

    def get_list_filter(self, request) -> Tuple[str, ...]:
        list_filter = super().get_list_filter(request)
        custom_fields = ("offschedule_datetime",)
        return custom_fields + tuple(f for f in list_filter if f not in custom_fields)


class OnScheduleModelAdmin(
    SiteModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    instructions = None

    fields = ("subject_identifier", "onschedule_datetime")

    def get_list_display(self, request) -> Tuple[str, ...]:
        list_display = super().get_list_display(request)
        custom_fields = ("subject_identifier", "dashboard", "onschedule_datetime")
        return custom_fields + tuple(
            f for f in list_display if f not in custom_fields + ("__str__",)
        )

    def get_list_filter(self, request) -> Tuple[str, ...]:
        list_filter = super().get_list_filter(request)
        custom_fields = ("onschedule_datetime",)
        return custom_fields + tuple(f for f in list_filter if f not in custom_fields)

    def get_readonly_fields(self, request, obj=None) -> Tuple[str, ...]:
        return (
            "subject_identifier",
            "onschedule_datetime",
        )

    def get_search_fields(self, request) -> Tuple[str, ...]:
        return tuple(set(super().get_search_fields(request) + ("subject_identifier",)))
