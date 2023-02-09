from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_model_admin.mixins import (
    ModelAdminFormAutoNumberMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminInstitutionMixin,
    TemplatesModelAdminMixin,
)

from ..admin_site import intecomm_group_admin
from ..forms import PatientGroupMeetingForm
from ..models import PatientGroupMeeting


@admin.register(PatientGroupMeeting, site=intecomm_group_admin)
class PatientGroupMeetingAdmin(
    TemplatesModelAdminMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin,
    ModelAdminRevisionMixin,
    ModelAdminInstitutionMixin,
    SimpleHistoryAdmin,
):
    form = PatientGroupMeetingForm

    show_object_tools = True
    change_list_template: str = "intecomm_group/admin/patientgroupmeeting_change_list.html"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "report_datetime",
                    "patient_group_appointment",
                    "meeting_datetime",
                )
            },
        ),
        (
            "Attendance",
            {"fields": ("patients",)},
        ),
        (
            "Notes",
            {"fields": ("notes",)},
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = ("patients",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        db = kwargs.get("using")
        if db_field.name == "patient_group_appointment" and request.GET.get(
            "patient_group_appointment"
        ):
            kwargs["queryset"] = db_field.related_model._default_manager.using(db).filter(
                pk=request.GET.get("patient_group_appointment")
            )
        else:
            kwargs["queryset"] = db_field.related_model._default_manager.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
