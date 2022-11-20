from typing import Tuple

from django.apps import apps as django_apps
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from ..admin_site import intecomm_screening_admin
from ..forms import PatientCallForm
from ..models import PatientCall
from .list_filters import AttendDatetListFilter
from .modeladmin_mixins import BaseModelAdminMixin


@admin.register(PatientCall, site=intecomm_screening_admin)
class PatientCallAdmin(BaseModelAdminMixin):
    form = PatientCallForm
    show_object_tools = False
    change_list_template: str = "intecomm_screening/admin/patientcall_change_list.html"

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
            "Details of call",
            {
                "fields": (
                    "answered",
                    "respondent",
                    "willing_to_attend",
                    "attend_date",
                    "call_again",
                )
            },
        ),
    )

    list_display = (
        "patient_log",
        "patient_log_link",
        "report_datetime",
        "answered",
        "willing_to_attend",
        "call_again",
        "attend_appt_date",
        "respondent",
    )

    list_filter = (
        "report_datetime",
        AttendDatetListFilter,
        "answered",
        "willing_to_attend",
        "call_again",
        "respondent",
    )

    radio_fields = {
        "answered": admin.VERTICAL,
        "respondent": admin.VERTICAL,
        "willing_to_attend": admin.VERTICAL,
        "call_again": admin.VERTICAL,
    }

    search_fields = (
        "patient_log__id",
        "patient_log__name__exact",
    )

    @admin.display(description="Attend Date", ordering="attend_date")
    def attend_appt_date(self, obj=None):
        return obj.attend_date

    @admin.display(description="Attend Date", ordering="attend_date")
    def patient_log_link(self, obj=None):
        url = reverse("intecomm_screening_admin:intecomm_screening_patientlog_changelist")
        url = f"{url}?q={obj.patient_log.id}"
        return format_html(f'<A href="{url}">patient log</a>')

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
