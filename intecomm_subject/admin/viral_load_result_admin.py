from django.contrib import admin
from edc_lab_results.fieldsets import BloodResultFieldset

from ..admin_site import intecomm_subject_admin
from ..forms import ViralLoadResultForm
from ..models import ViralLoadResult
from .modeladmin_mixins import CrfModelAdmin


@admin.register(ViralLoadResult, site=intecomm_subject_admin)
class ViralLoadResultAdmin(CrfModelAdmin):
    form = ViralLoadResultForm
    autocomplete_fields = ["requisition"]
    fieldsets = BloodResultFieldset(
        ViralLoadResult.lab_panel,
        model_cls=ViralLoadResult,
        exclude_units=True,
        exclude_reportable=True,
    ).fieldsets
