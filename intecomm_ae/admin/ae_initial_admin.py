from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_action_item import action_fieldset_tuple
from edc_adverse_event.modeladmin_mixins import (
    AeInitialModelAdminMixin,
    fieldset_part_three,
)
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import intecomm_ae_admin
from ..forms import AeInitialForm
from ..models import AeInitial


@admin.register(AeInitial, site=intecomm_ae_admin)
class AeInitialAdmin(SiteModelAdminMixin, AeInitialModelAdminMixin, SimpleHistoryAdmin):
    form = AeInitialForm
    additional_instructions = None

    fieldsets = (
        (None, {"fields": ("subject_identifier", "report_datetime")}),
        (
            "Part 1: Description",
            {
                "fields": (
                    "ae_classification_as_text",
                    "ae_description",
                    "ae_awareness_date",
                    "ae_start_date",
                    "ae_grade",
                )
            },
        ),
        fieldset_part_three,
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "ae_grade": admin.VERTICAL,
    }

    def get_list_filter(self, request) -> tuple[str, ...]:
        list_filter = super().get_list_filter(request)
        custom_fields = ("ae_awareness_date", "ae_grade")
        excluded_fields = [
            "ae_classification",
            "sae",
            "sae_reason",
            "susar",
            "susar_reported",
        ]
        excluded_fields.extend(custom_fields)
        list_filter = custom_fields + tuple(f for f in list_filter if f not in excluded_fields)
        # TODO: remove with Django > 4.2.5
        self.list_filter = list_filter
        return list_filter
