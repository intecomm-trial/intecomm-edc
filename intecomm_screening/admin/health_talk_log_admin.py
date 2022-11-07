from django.contrib import admin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_model_admin.mixins import (
    ModelAdminFormAutoNumberMixin,
    ModelAdminFormInstructionsMixin,
    TemplatesModelAdminMixin,
)
from edc_sites import get_site_name

from intecomm_sites import all_sites

from ..admin_site import intecomm_screening_admin
from ..forms import HealthTalkLogForm
from ..models import HealthTalkLog


@admin.register(HealthTalkLog, site=intecomm_screening_admin)
class HealthTalkLogAdmin(
    TemplatesModelAdminMixin,
    ModelAdminFormAutoNumberMixin,
    ModelAdminFormInstructionsMixin,
    SimpleHistoryAdmin,
):
    form = HealthTalkLogForm
    show_object_tools = True
    change_list_template: str = "intecomm_screening/admin/healthtalklog_change_list.html"

    fieldsets = (
        (
            None,
            {"fields": ("report_date",)},
        ),
        (
            "Details of talk",
            {
                "fields": (
                    "health_facility_name",
                    "health_facility",
                    "health_facility_other",
                    "health_talk_type",
                    "health_talk_type_other",
                    "number_attended",
                    "notes",
                )
            },
        ),
    )

    list_display = (
        "report_date",
        "site",
        "health_facility_name",
        "health_facility",
        "health_talk_type",
        "number_attended",
    )

    list_filter = (
        "report_date",
        "health_facility",
        "health_talk_type",
    )

    radio_fields = {
        "health_facility": admin.VERTICAL,
        "health_talk_type": admin.VERTICAL,
    }

    search_fields = (
        "health_facility__name",
        "patient_log__name__exact",
    )

    def site_name(self, obj=None):
        get_site_name.get(obj.site.id, all_sites)
        return obj.name
