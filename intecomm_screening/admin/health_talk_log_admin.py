from django.contrib import admin
from django.utils.html import format_html
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
    change_list_title = HealthTalkLog._meta.verbose_name

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
        "health_facility",
        "health_talk_type",
        "map",
        "attended",
    )

    list_filter = (
        "report_date",
        "health_talk_type",
        "health_facility",
    )

    radio_fields = {
        "health_talk_type": admin.VERTICAL,
    }

    search_fields = (
        "health_facility__name",
        "health_facility__health_facility_type__name",
        "patient_log__legal_name__exact",
        "patient_log__familiar_name__exact",
    )

    @admin.display(description="Attended", ordering="number_attended")
    def attended(self, obj=None):
        return obj.number_attended

    @staticmethod
    def site_name(obj=None):
        get_site_name(obj.site.id, all_sites)
        return obj.name

    @admin.display(description="Map")
    def map(self, obj=None):
        if obj.health_facility.latitude and obj.health_facility.longitude:
            return format_html(
                f'<A href="https://www.google.com/maps/@{obj.health_facility.latitude},"'
                f'"{obj.health_facility.longitude},15z">'
                '<i class="fas fa-location-dot"></i>'
            )
        return None
