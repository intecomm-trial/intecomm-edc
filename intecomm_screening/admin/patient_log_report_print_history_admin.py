from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple

from ..admin_site import intecomm_screening_admin
from ..models import PatientLogReportPrintHistory
from .modeladmin_mixins import BaseModelAdminMixin


@admin.register(PatientLogReportPrintHistory, site=intecomm_screening_admin)
class PatientLogReportPrintHistoryAdmin(BaseModelAdminMixin):
    show_object_tools = False

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "patient_log_identifier",
                    "printed_datetime",
                    "printed_user",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = ("patient_log_identifier", "printed_datetime", "printed_user")
    list_filter = ("printed_datetime", "printed_user")
    search_fields = ("patient_log_identifier",)
    readonly_fields = ("patient_log_identifier", "printed_datetime", "printed_user")
