from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_qol.modeladmin_mixins import icecapa_fieldsets, icecapa_radio_fields

from ..admin_site import intecomm_subject_admin
from ..forms import IcecapaForm
from ..models import Icecapa
from .modeladmin_mixins import CrfModelAdmin


@admin.register(Icecapa, site=intecomm_subject_admin)
class IcecapaModelAdmin(CrfModelAdmin):
    form = IcecapaForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        *icecapa_fieldsets(),
        audit_fieldset_tuple,
    )

    radio_fields = icecapa_radio_fields()
