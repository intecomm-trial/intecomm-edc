from django.contrib import admin

from ..admin_site import intecomm_reports_admin
from ..models import VlSummary9m
from .modeladmin_mixins import VlSummaryModelAdminMixin


@admin.register(VlSummary9m, site=intecomm_reports_admin)
class VlSummary9mAdmin(VlSummaryModelAdminMixin, admin.ModelAdmin):

    report_model = "intecomm_reports.vlsummary9m"
    endline_months = 9
