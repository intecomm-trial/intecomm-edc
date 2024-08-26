from django.contrib import admin

from ..admin_site import intecomm_reports_admin
from ..models import VlSummary6m
from .modeladmin_mixins import VlSummaryModelAdminMixin


@admin.register(VlSummary6m, site=intecomm_reports_admin)
class VlSummary6mAdmin(VlSummaryModelAdminMixin, admin.ModelAdmin):

    report_model = "intecomm_reports.vlsummary6m"
    endline_months = 6
