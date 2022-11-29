from typing import Tuple

from django.apps import apps as django_apps
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from ..admin_site import intecomm_screening_admin
from ..forms import PatientCallForm
from ..models import PatientCall
from .list_filters import LastApptListFilter, NextApptListFilter
from .modeladmin_mixins import BaseModelAdminMixin


@admin.register(PatientCall, site=intecomm_screening_admin)
class PatientCallAdmin(BaseModelAdminMixin):
    form = PatientCallForm
    show_object_tools = False
    change_list_template: str = "intecomm_screening/admin/patientcall_change_list.html"
    change_list_title = PatientCall._meta.verbose_name

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
        url = reverse("intecomm_screening_admin:intecomm_screening_patientlog_changelist")
        url = f"{url}?q={obj.patient_log.id}"
        return format_html(f'<A href="{url}">{obj.patient_log}</a>')

    @property
    def patient_log_model_cls(self):
        return django_apps.get_model("intecomm_screening.patientlog")

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

    @admin.display(description="Alive", ordering="survival_status")
    def alive(self, obj=None):
        return obj.survival_status

    @admin.display(description="In Area", ordering="catchment_area")
    def in_area(self, obj=None):
        return obj.catchment_area
