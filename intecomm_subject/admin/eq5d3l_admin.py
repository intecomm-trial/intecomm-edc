from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_qol.modeladmin_mixins import eq5d3l_fieldsets, eq5d3l_radio_fields

from ..admin_site import intecomm_subject_admin
from ..forms import Eq5d3lForm
from ..models import Eq5d3l
from .modeladmin_mixins import CrfModelAdmin


@admin.register(Eq5d3l, site=intecomm_subject_admin)
class Eq5d3lAdmin(CrfModelAdmin):
    form = Eq5d3lForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        *eq5d3l_fieldsets(),
        audit_fieldset_tuple,
    )

    radio_fields = eq5d3l_radio_fields()
