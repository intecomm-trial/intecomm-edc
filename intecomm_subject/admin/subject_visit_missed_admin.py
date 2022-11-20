from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..forms import SubjectVisitMissedForm
from ..models import SubjectVisitMissed
from .modeladmin_mixins import CrfModelAdmin


@admin.register(SubjectVisitMissed, site=intecomm_subject_admin)
class SubjectVisitMissedAdmin(CrfModelAdmin):

    form = SubjectVisitMissedForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Contact History",
            {
                "fields": (
                    "survival_status",
                    "contact_attempted",
                    "contact_made",
                    "contact_attempts_count",
                    "contact_attempts_explained",
                    "contact_last_date",
                    "missed_reasons",
                    "missed_reasons_other",
                    "comment",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = ("missed_reasons",)

    radio_fields = {
        "survival_status": admin.VERTICAL,
        "contact_attempted": admin.VERTICAL,
        "contact_made": admin.VERTICAL,
    }
