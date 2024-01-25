from django.contrib import admin
from django.contrib.admin import display
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_adverse_event.modeladmin_mixins import DeathReportModelAdminMixin
from edc_adverse_event.modeladmin_mixins.list_filters import CauseOfDeathListFilter
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import intecomm_ae_admin
from ..forms import DeathReportForm
from ..models import DeathReport


@admin.register(DeathReport, site=intecomm_ae_admin)
class DeathReportAdmin(SiteModelAdminMixin, DeathReportModelAdminMixin, SimpleHistoryAdmin):
    form = DeathReportForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_identifier",
                    "report_datetime",
                    "death_datetime",
                )
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "death_as_inpatient",
                    "death_location",
                    "hospital_name",
                )
            },
        ),
        (
            "Informant Information",
            {
                "fields": (
                    "informant_contact",
                    "informant_relationship",
                    "other_informant_relationship",
                )
            },
        ),
        (
            "Cause of death",
            {
                "description": (
                    "If death occurred in hospital or a death certificate is available, "
                    "please indicate the recorded causes of death"
                ),
                "fields": (
                    "death_certificate",
                    "cause_of_death",
                    "narrative",
                ),
            },
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "death_as_inpatient": admin.VERTICAL,
        "death_location": admin.VERTICAL,
        "informant_relationship": admin.VERTICAL,
        "death_certificate": admin.VERTICAL,
    }

    def get_list_filter(self, request) -> tuple[str, ...]:
        list_filter = super().get_list_filter(request)
        list_filter = list(list_filter)
        index = list_filter.index(CauseOfDeathListFilter)
        list_filter.remove(CauseOfDeathListFilter)
        list_filter.insert(index, "cause_of_death")
        list_filter = tuple(list_filter)
        return list_filter

    @display(
        description="Cause of death",
        ordering="cause_of_death",
    )
    def cause_of_death_column(self, obj):
        return obj.cause_of_death
