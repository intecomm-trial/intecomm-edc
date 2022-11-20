from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..models import Hba1cResult
from .modeladmin_mixins import CrfModelAdmin


@admin.register(Hba1cResult, site=intecomm_subject_admin)
class Hba1cResultAdmin(CrfModelAdmin):
    # form = Hba1cResultForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        ("Result", {"fields": ("drawn_date", "result")}),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
    }
