from typing import Tuple

from django.apps import apps as django_apps
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from edc_model_admin.mixins import ModelAdminLimitToSelectedForeignkey
from edc_sites.admin import SiteModelAdminMixin
from intecomm_rando.constants import UGANDA

from ..admin_site import intecomm_screening_admin
from ..forms import PatientCallForm
from ..models import PatientCall, PatientLog
from .list_filters import LastApptListFilter, NextApptListFilter
from .modeladmin_mixins import (
    BaseModelAdminMixin,
    ChangeListTopBarModelAdminMixin,
    RedirectAllToPatientLogModelAdminMixin,
)


@admin.register(PatientCall, site=intecomm_screening_admin)
class PatientCallAdmin(
    SiteModelAdminMixin,
    ModelAdminLimitToSelectedForeignkey,
    RedirectAllToPatientLogModelAdminMixin,
    ChangeListTopBarModelAdminMixin,
    BaseModelAdminMixin,
):
    form = PatientCallForm
    show_object_tools = True
    list_per_page = 5
    ordering = ("site__id", "report_datetime")

    # TemplatesModelAdminMixin attr
    change_list_template: str = "intecomm_screening/admin/patientcall_change_list.html"
    change_list_title = PatientCall._meta.verbose_name

    # ChangeListTopBarModelAdminMixin attrs
    changelist_top_bar_selected = "patientcall"
    changelist_top_bar_add_url = "intecomm_screening_admin:intecomm_screening_patientcall_add"

    # RedirectAllToPatientLogModelAdminMixin attrs
    change_search_field_name = "patient_log__patient_log_identifier"
    add_search_field_name = "patient_log__patient_log_identifier"

    # SiteModelAdminMixin attr
    limit_related_to_current_site = ["patient_log"]

    # ModelAdminLimitToSelectedForeignkey attrs
    limit_fk_field_to_selected = [("patient_log", PatientLog)]

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
            "Patient Status",
            {
                "fields": (
                    "answered",
                    "respondent",
                    "survival_status",
                    "catchment_area",
                )
            },
        ),
        (
            "Patient Care",
            {
                "fields": (
                    "last_appt_date",
                    "last_attend_clinic",
                    # "last_attend_clinic_other",
                    "next_appt_date",
                )
            },
        ),
        (
            "Notes and followup",
            {
                "fields": (
                    "call_again",
                    "comment",
                )
            },
        ),
    )

    list_display = (
        "report_datetime",
        "patient_log_link",
        "answered",
        "respondent",
        "alive",
        "in_area",
        "call_again",
        "last_appt",
        "next_appt",
    )

    list_filter = (
        "report_datetime",
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
        "patient_log__id",
        "patient_log__legal_name__exact",
        "patient_log__familiar_name__exact",
    )

    @admin.display(description="Last Appt", ordering="last_appt_date")
    def last_appt(self, obj=None):
        return obj.last_appt_date

    @admin.display(description="Next Appt", ordering="next_appt_date")
    def next_appt(self, obj=None):
        return obj.next_appt_date

    @admin.display(description="Patient", ordering="patient_log")
    def patient_log_link(self, obj=None):
        if obj.site.siteprofile.country == UGANDA:
            url = reverse(
                "intecomm_screening_admin:intecomm_screening_patientlogug_changelist"
            )
        else:
            url = reverse("intecomm_screening_admin:intecomm_screening_patientlog_changelist")
        url = f"{url}?q={obj.patient_log.id}"
        return format_html(f'<A href="{url}">{obj.patient_log}</a>')

    @property
    def patient_log_model_cls(self):
        return django_apps.get_model("intecomm_screening.patientlog")

    @admin.display(description="Alive", ordering="survival_status")
    def alive(self, obj=None):
        return obj.survival_status

    @admin.display(description="In Area", ordering="catchment_area")
    def in_area(self, obj=None):
        return obj.catchment_area

    def get_readonly_fields(self, request, obj=None) -> Tuple[str, ...]:
        readonly = super().get_readonly_fields(request, obj=obj)
        if obj and "patient_log" not in readonly:
            readonly = readonly + ("patient_log",)
        return readonly
