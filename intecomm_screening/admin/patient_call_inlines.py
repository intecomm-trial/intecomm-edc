from django.contrib import admin
from django_audit_fields import ModelAdminAuditFieldsMixin

from ..forms import PatientCallForm
from ..models import PatientCall


class PatientCallInlineMixin:
    model = PatientCall
    form = PatientCallForm
    extra = 0
    readonly_fields = ["report_datetime"]
    radio_fields = {
        "answered": admin.VERTICAL,
        "respondent": admin.VERTICAL,
        "survival_status": admin.VERTICAL,
        "catchment_area": admin.VERTICAL,
        "call_again": admin.VERTICAL,
    }


class AddPatientCallInline(
    ModelAdminAuditFieldsMixin, PatientCallInlineMixin, admin.StackedInline
):
    fieldsets = (
        [None, {"fields": ("report_datetime",)}],
        (
            "Details of the call",
            {
                "fields": (
                    "answered",
                    "respondent",
                    "survival_status",
                    "catchment_area",
                    "last_appt_date",
                    "next_appt_date",
                    "call_again",
                    "comment",
                ),
            },
        ),
    )
    verbose_name = "New Call"
    verbose_name_plural = "New Calls"

    def has_change_permission(self, request, obj=None):
        return True

    def get_queryset(self, request):
        return PatientCall.objects.none()


class ViewPatientCallInline(
    ModelAdminAuditFieldsMixin, PatientCallInlineMixin, admin.StackedInline
):
    fieldsets = (
        (
            "Details of the call",
            {
                "classes": ("collapse",),
                "fields": (
                    "report_datetime",
                    "respondent",
                    "survival_status",
                    "catchment_area",
                    "last_appt_date",
                    "next_appt_date",
                    "comment",
                ),
            },
        ),
    )
    verbose_name = "Past Call"
    verbose_name_plural = "Past Calls"

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False
