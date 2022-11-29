from django.contrib import admin
from edc_lab_results.fieldsets import BloodResultFieldset

from ..admin_site import intecomm_subject_admin
from ..forms import Cd4ResultForm
from ..models import Cd4Result
from .modeladmin_mixins import CrfModelAdmin


@admin.register(Cd4Result, site=intecomm_subject_admin)
class Cd4ResultAdmin(CrfModelAdmin):
    form = Cd4ResultForm
    autocomplete_fields = ["requisition"]
    fieldsets = BloodResultFieldset(
        Cd4Result.lab_panel,
        model_cls=Cd4Result,
        exclude_units=True,
        exclude_reportable=True,
    ).fieldsets
