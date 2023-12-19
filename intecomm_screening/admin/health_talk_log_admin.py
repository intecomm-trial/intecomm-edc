from django.contrib import admin
from django.utils.html import format_html
from edc_sites.admin import SiteModelAdminMixin

from intecomm_facility.models import HealthFacility

from ..admin_site import intecomm_screening_admin
from ..forms import HealthTalkLogForm
from ..models import HealthTalkLog
from .modeladmin_mixins import BaseModelAdminMixin, ChangeListTopBarModelAdminMixin


@admin.register(HealthTalkLog, site=intecomm_screening_admin)
class HealthTalkLogAdmin(
    SiteModelAdminMixin, ChangeListTopBarModelAdminMixin, BaseModelAdminMixin
):
    form = HealthTalkLogForm
    show_object_tools = True
    list_per_page = 5
    ordering = ("site__id", "report_date")

    # TemplatesModelAdminMixin attrs
    change_list_template: str = "intecomm_screening/admin/healthtalklog_change_list.html"
    change_list_title = HealthTalkLog._meta.verbose_name

    # ChangeListTopBarModelAdminMixin attrs
    changelist_top_bar_selected = "healthtalklog"
    changelist_top_bar_add_url = (
        "intecomm_screening_admin:intecomm_screening_healthtalklog_add"
    )

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

    @admin.display(description="Map")
    def map(self, obj=None):
        if obj.health_facility.latitude and obj.health_facility.longitude:
            return format_html(
                f'<A href="https://www.google.com/maps/@{obj.health_facility.latitude},"'
                f'"{obj.health_facility.longitude},15z">'
                '<i class="fas fa-location-dot"></i>'
            )
        return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "health_facility":
            try:
                site_id = request.site.id
            except AttributeError:
                pass
            else:
                kwargs["queryset"] = HealthFacility.objects.filter(site_id=site_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
