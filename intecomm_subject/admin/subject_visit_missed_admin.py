from copy import copy

from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item import action_fields, action_fieldset_tuple
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import intecomm_subject_admin
# from ..forms import SubjectVisitMissedForm
from ..models import SubjectVisitMissed
from .modeladmin_mixins import CrfModelAdmin


@admin.register(SubjectVisitMissed, site=intecomm_subject_admin)
class SubjectVisitMissedAdmin(CrfModelAdmin, FormLabelModelAdminMixin, SimpleHistoryAdmin):

    # form = SubjectVisitMissedForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Contact History",
            {
                "fields": (
                    "survival_status",
                    "contact_attempted",
                    "contact_attempts_count",
                    "contact_made",
                    "contact_attempts_explained",
                    "contact_last_date",
                    "missed_reasons",
                    "missed_reasons_other",
                    "ltfu",
                    "comment",
                ),
            },
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = ("missed_reasons",)

    radio_fields = {
        "survival_status": admin.VERTICAL,
        "contact_attempted": admin.VERTICAL,
        "contact_made": admin.VERTICAL,
        "ltfu": admin.VERTICAL,
    }

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        action_flds = copy(list(action_fields))
        fields = list(action_flds) + list(fields)
        return fields
