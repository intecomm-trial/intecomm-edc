from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..forms import ClinicalNoteForm
from ..models import ClinicalNote
from .modeladmin_mixins import CrfModelAdmin


@admin.register(ClinicalNote, site=intecomm_subject_admin)
class ClinicalNoteAdmin(CrfModelAdmin):
    form = ClinicalNoteForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        ("Notes", {"fields": ("has_comment", "comments")}),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "has_comment": admin.VERTICAL,
    }
