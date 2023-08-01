from typing import Tuple

from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import ModelAdminRedirectAllToChangelistMixin
from edc_registration.models import RegisteredSubject
from edc_sites.admin import SiteModelAdminMixin
from edc_utils import convert_php_dateformat
from edc_utils.date import to_local

from intecomm_screening.admin.list_filters import LastApptListFilter, NextApptListFilter
from intecomm_screening.admin.modeladmin_mixins import BaseModelAdminMixin

from ..admin_site import intecomm_group_admin
from ..forms import PatientFollowupCallForm
from ..models import PatientFollowupCall
from .list_filters import PatientGroupLastCallListFilter


@admin.register(PatientFollowupCall, site=intecomm_group_admin)
class PatientFollowupCallAdmin(
    ModelAdminRedirectAllToChangelistMixin,
    ModelAdminDashboardMixin,
    SiteModelAdminMixin,
    BaseModelAdminMixin,
):
    form = PatientFollowupCallForm
    show_object_tools = False
    change_list_template: str = "intecomm_group/admin/patientfollowupcall_change_list.html"
    ordering = ["-report_datetime", "patient_log__subject_identifier"]

    changelist_url = "intecomm_group_admin:intecomm_group_patientfollowupcall_changelist"
    change_search_field_name = "patient_log__subject_identifier"
    add_search_field_name = "patient_log"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "patient_log",
                    "report_datetime",
                )
            },
        ),
        (
            "Contact numbers",
            {
                "fields": (
                    "contact_number",
                    "alt_contact_number",
                )
            },
        ),
        (
            "Details of call",
            {
                "fields": (
                    "answered",
                    "respondent",
                    "call_again",
                    "survival_status",
                    "catchment_area",
                    "last_appt_date",
                    "next_appt_date",
                    "comment",
                )
            },
        ),
    )

    list_display = (
        "subject_identifier",
        "dashboard",
        "subject_locator",
        "call_summary",
        "last_appt",
        "next_appt",
    )

    list_filter = (
        PatientGroupLastCallListFilter,
        LastApptListFilter,
        NextApptListFilter,
        "answered",
        "call_again",
        "respondent",
        "survival_status",
        "catchment_area",
    )

    radio_fields = {
        "answered": admin.VERTICAL,
        "respondent": admin.VERTICAL,
        "survival_status": admin.VERTICAL,
        "catchment_area": admin.VERTICAL,
        "call_again": admin.VERTICAL,
    }

    search_fields = (
        "patient_log__subject_identifier",
        "patient_log__id",
        "patient_log__legal_name__exact",
        "patient_log__familiar_name__exact",
    )

    @admin.display(description="Patient", ordering="patient_log")
    def patient_log_link(self, obj=None):
        url = reverse("intecomm_screening_admin:intecomm_screening_patientlog_changelist")
        url = f"{url}?q={obj.patient_log.id}"
        return format_html(f'<A href="{url}">{obj.patient_log}</a>')

    @property
    def patient_log_model_cls(self):
        return django_apps.get_model("intecomm_screening.patientlog")

    @admin.display(description="Locator", ordering="subject_identifier")
    def subject_locator(self, obj=None):
        url = reverse("intecomm_prn_admin:intecomm_prn_subjectlocator_changelist")
        context = dict(url=f"{url}?q={obj.patient_log.subject_identifier}")
        return render_to_string(
            "intecomm_group/patient_followup_call_locator.html", context=context
        )

    @admin.display(description="Summary", ordering="report_datetime")
    def call_summary(self, obj=None):
        date_format = convert_php_dateformat(settings.SHORT_DATE_FORMAT)
        context = dict(
            last_call=to_local(obj.report_datetime).date().strftime(date_format),
            answered=obj.answered,
            survival_status=obj.survival_status,
            catchment_area=obj.catchment_area,
            call_again=obj.call_again,
            respondent=obj.get_respondent_display(),
        )
        return render_to_string(
            "intecomm_group/patient_followup_call_summary.html", context=context
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "patient_log":
            if request.GET.get("patient_log"):
                kwargs["queryset"] = self.patient_log_model_cls.objects.filter(
                    id__exact=request.GET.get("patient_log", 0)
                )
            else:
                kwargs["queryset"] = self.patient_log_model_cls.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None) -> Tuple[str, ...]:
        readonly = super().get_readonly_fields(request, obj=obj)
        if obj and "patient_log" not in readonly:
            readonly = readonly + ("patient_log",)
        return readonly

    @admin.display(
        description="Subject identifier", ordering="patient_log__subject_identifier"
    )
    def subject_identifier(self, obj):
        return obj.patient_log.subject_identifier

    def get_subject_dashboard_url_kwargs(self, obj) -> dict:
        return dict(subject_identifier=obj.patient_log.subject_identifier)

    def get_registered_subject(self, obj) -> RegisteredSubject:
        return RegisteredSubject.objects.get(
            subject_identifier=obj.patient_log.subject_identifier
        )

    @admin.display(description="Alive", ordering="survival_status")
    def alive(self, obj):
        return obj.survival_status

    @admin.display(description="Catchment", ordering="catchment_area")
    def in_catchment_area(self, obj):
        return obj.catchment_area

    @admin.display(description="Call again?", ordering="call_again")
    def may_call_again(self, obj):
        return obj.call_again

    @admin.display(description="Last appt", ordering="last_appt_date")
    def last_appt(self, obj):
        if obj.last_appt_date:
            date_format = convert_php_dateformat(settings.SHORT_DATE_FORMAT)
            return format_html(
                f'<span style="white-space:nowrap;">'
                f"{obj.last_appt_date.strftime(date_format)}</span>"
            )
        return None

    @admin.display(description="Next appt", ordering="next_appt_date")
    def next_appt(self, obj):
        if obj.next_appt_date:
            date_format = convert_php_dateformat(settings.SHORT_DATE_FORMAT)
            return format_html(
                f'<span style="white-space:nowrap;">'
                f"{obj.next_appt_date.strftime(date_format)}</span>"
            )
        return None
