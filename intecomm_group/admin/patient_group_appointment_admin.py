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
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import intecomm_group_admin
from ..forms import PatientGroupAppointmentForm
from ..models import PatientGroupAppointment


@admin.register(PatientGroupAppointment, site=intecomm_group_admin)
class PatientGroupAppointmentAdmin(
    SiteModelAdminMixin,
    TemplatesModelAdminMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin,
    ModelAdminRevisionMixin,
    ModelAdminInstitutionMixin,
    SimpleHistoryAdmin,
):
    form = PatientGroupAppointmentForm

    limit_related_to_current_site = ["patient_group", "community_care_location"]

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
