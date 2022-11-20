from django.contrib import admin
from edc_sites import get_site_name

from intecomm_sites import all_sites

from ..admin_site import intecomm_screening_admin
from ..forms import HealthTalkLogForm
from ..models import HealthTalkLog
from .modeladmin_mixins import BaseModelAdminMixin


@admin.register(HealthTalkLog, site=intecomm_screening_admin)
class HealthTalkLogAdmin(BaseModelAdminMixin):
    form = HealthTalkLogForm
    show_object_tools = True
    change_list_template: str = "intecomm_screening/admin/healthtalklog_change_list.html"

    autocomplete_fields = ["health_facility"]

    fieldsets = (
        (
            None,
            {"fields": ("report_date",)},
        ),
        (
            "Details of talk",
            {
                "fields": (
                    "health_facility",
                    "health_facility_type",
                    "health_facility_type_other",
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
        "site_name",
        "health_facility",
        "health_facility_type",
        "health_talk_type",
        "number_attended",
    )

    list_filter = (
        "report_date",
        "health_facility_type",
        "health_talk_type",
    )

    radio_fields = {
        "health_facility_type": admin.VERTICAL,
        "health_talk_type": admin.VERTICAL,
    }

    search_fields = (
        "health_facility__name",
        "health_facility_type__name",
        "patient_log__name__exact",
    )

    @staticmethod
    def site_name(obj=None):
        get_site_name(obj.site.id, all_sites)
        return obj.name
