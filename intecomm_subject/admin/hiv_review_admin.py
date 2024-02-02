from __future__ import annotations

from typing import TYPE_CHECKING, Type

from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..forms import HivReviewForm
from ..models import HivReview
from .fieldsets import care_delivery_fieldset_tuple
from .list_filters import VlStatusListFilter
from .modeladmin_mixins import CrfModelAdmin

if TYPE_CHECKING:
    from django.contrib.admin import SimpleListFilter


@admin.register(HivReview, site=intecomm_subject_admin)
class HivReviewAdmin(CrfModelAdmin):
    form = HivReviewForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        care_delivery_fieldset_tuple,
        (
            "Anti-retroviral therapy (ART)",
            {
                "fields": (
                    "rx_init",
                    "rx_init_date",
                    "rx_init_ago",
                )
            },
        ),
        (
            "Monitoring",
            {
                "fields": (
                    "has_vl",
                    "drawn_date",
                    "vl",
                    "vl_quantifier",
                ),
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "rx_init": admin.VERTICAL,
        "care_delivery": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
        "dx": admin.VERTICAL,
        "has_vl": admin.VERTICAL,
        "vl_quantifier": admin.VERTICAL,
    }

    @admin.display(description="VL resulted", ordering="has_vl")
    def vl_status(self, obj):
        return obj.has_vl

    def get_list_filter(self, request) -> tuple[str | Type[SimpleListFilter], ...]:
        list_filters = super().get_list_filter(request)
        list_filters = list(list_filters) or []
        list_filters.insert(4, VlStatusListFilter)
        return tuple(list_filters)

    def get_list_display(self, request) -> tuple[str, ...]:
        list_display = super().get_list_display(request)
        list_display = list(list_display) or []
        list_display.insert(4, "vl_status")
        return tuple(list_display)
