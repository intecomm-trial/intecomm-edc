from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_model_admin.mixins import (
    ModelAdminFormAutoNumberMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminInstitutionMixin,
    TemplatesModelAdminMixin,
)

from ..admin_site import intecomm_screening_admin
from ..forms import PatientGroupForm
from ..models import PatientGroup


@admin.register(PatientGroup, site=intecomm_screening_admin)
class PatientGroupAdmin(
    TemplatesModelAdminMixin,
    ModelAdminFormInstructionsMixin,  # add
    ModelAdminFormAutoNumberMixin,
    ModelAdminRevisionMixin,  # add
    ModelAdminInstitutionMixin,  # add
    SimpleHistoryAdmin,
):

    form = PatientGroupForm

    show_object_tools = True

    fieldsets = (
        (
            None,
            {"fields": ("report_datetime", "name", "patients", "notes")},
        ),
        (
            "Status",
            {"fields": ("status", "randomize")},
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "name",
        "opened",
        "status",
        "arm",
        "members",
        "user_created",
        "created",
    )

    list_filter = (
        "status",
        "report_datetime",
    )

    search_fields = (
        "name",
        "patients__name",
    )

    filter_horizontal = ("patients",)

    radio_fields = {
        "status": admin.VERTICAL,
        "randomize": admin.VERTICAL,
    }

    @admin.display(description="Opened", ordering="report_datetime")
    def opened(self, obj=None):
        return obj.report_datetime.date()

    @admin.display(description="Members")
    def members(self, obj=None):
        cnt = obj.patients.all().count()
        url = reverse("intecomm_screening_admin:intecomm_screening_patientlog_changelist")
        url = f"{url}?q={obj.name}"
        return format_html(f'<a href="{url}">{cnt} patients</a>')

    @admin.display(description="Arm")
    def arm(self, obj=None):
        # site_randomizers.get("intecomm") INTE or COMM
        return None
