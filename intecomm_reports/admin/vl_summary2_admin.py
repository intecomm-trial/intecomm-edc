from django.contrib import admin
from django.db.models import Q, QuerySet

from ..admin_site import intecomm_reports_admin
from ..models import VlSummary2
from ..vl_summary import VlSummary
from .vl_summary_admin import VlSummaryAdmin


@admin.register(VlSummary2, site=intecomm_reports_admin)
class VlSummary2Admin(VlSummaryAdmin):

    def get_queryset(self, request) -> QuerySet:
        vl_summary = VlSummary(endline_months=6, skip_update_dx=True)
        vl_summary.to_model(model="intecomm_reports.vlsummary2")
        qs = super().get_queryset(request)
        return qs.filter((Q(baseline_vl__isnull=True) | Q(endline_vl__isnull=True)))
