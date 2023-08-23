from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..forms import LocationUpdateForm
from ..models import LocationUpdate
from .modeladmin_mixins import CrfModelAdmin


@admin.register(LocationUpdate, site=intecomm_subject_admin)
class LocationUpdateAdmin(CrfModelAdmin):
    form = LocationUpdateForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        ("Update", {"fields": ("location", "location_other", "comments", "next_location")}),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "location": admin.VERTICAL,
        "next_location": admin.VERTICAL,
    }
