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
from ..forms import PatientGroupAppointmentForm
from ..models import PatientGroupAppointment


@admin.register(PatientGroupAppointment, site=intecomm_group_admin)
class PatientGroupAppointmentAdmin(
    TemplatesModelAdminMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin,
    ModelAdminRevisionMixin,
    ModelAdminInstitutionMixin,
    SimpleHistoryAdmin,
):

    form = PatientGroupAppointmentForm

    show_object_tools = True
    change_list_template: str = "intecomm_group/admin/patientgroupappointment_change_list.html"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "report_datetime",
                    "patient_group",
                    "community_care_location",
                    "appt_datetime",
                    "appt_status",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {"appt_status": admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        db = kwargs.get("using")
        if db_field.name == "patient_group" and request.GET.get("patient_group"):
            kwargs["queryset"] = db_field.related_model._default_manager.using(db).filter(
                pk=request.GET.get("patient_group")
            )
        else:
            kwargs["queryset"] = db_field.related_model._default_manager.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
