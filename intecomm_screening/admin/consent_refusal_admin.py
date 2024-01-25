from __future__ import annotations

from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import intecomm_screening_admin
from ..forms import ConsentRefusalForm
from ..models import ConsentRefusal
from .modeladmin_mixins import (
    BaseModelAdminMixin,
    RedirectAllToPatientLogModelAdminMixin,
)


@admin.register(ConsentRefusal, site=intecomm_screening_admin)
class ConsentRefusalAdmin(
    SiteModelAdminMixin,
    RedirectAllToPatientLogModelAdminMixin,
    BaseModelAdminMixin,
):
    form = ConsentRefusalForm
    show_object_tools = True
    list_per_page = 5
    ordering = ("site__id", "screening_identifier")

    fieldsets = (
        [
            None,
            {
                "fields": (
                    "screening_identifier",
                    "report_datetime",
                    "reason",
                    "other_reason",
                )
            },
        ],
        (
            "Screening",
            {"classes": ("collapse",), "fields": ("subject_screening",)},
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "subject_screening",
        "report_datetime",
        "reason",
        "user_created",
        "created",
    )

    list_filter = ("report_datetime", "subject_screening__gender", "reason")

    search_fields = (
        "screening_identifier",
        "subject_screening__hospital_identifier",
        "subject_screening__initials",
    )

    radio_fields = {
        "reason": admin.VERTICAL,
    }

    readonly_fields = ("subject_screening",)
