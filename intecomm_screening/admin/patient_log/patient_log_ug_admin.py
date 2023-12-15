from __future__ import annotations

from django.apps import apps as django_apps
from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.mixins import ModelAdminRedirectAllToChangelistMixin

from ...admin_site import intecomm_screening_admin
from ...forms import PatientLogUgForm
from ...models import PatientLogUg
from ..modeladmin_mixins import BaseModelAdminMixin
from .fieldsets import (
    get_address_fielset,
    get_appointment_fieldset,
    get_contact_fieldset,
    get_first_fieldset,
    get_group_fieldset,
    get_health_fieldset,
    get_health_talks_fieldset,
    get_names_and_basic_demographics_fieldset,
    get_screening_and_consent_fieldset,
    get_willingness_to_screen_fieldset,
)
from .get_search_fields import get_search_fields
from .modeladmin_mixins import PatientLogModelAdminMixin


@admin.register(PatientLogUg, site=intecomm_screening_admin)
class PatientLogUgAdmin(
    PatientLogModelAdminMixin,
    ModelAdminRedirectAllToChangelistMixin,
    BaseModelAdminMixin,
):
    changelist_top_bar_selected = "patientlog"
    changelist_top_bar_add_url = "intecomm_screening_admin:intecomm_screening_patientlogug_add"
    change_list_template: str = "intecomm_screening/admin/patientlog_change_list.html"

    # ModelAdminRedirectAllToChangelistMixin
    changelist_url = "intecomm_screening_admin:intecomm_screening_patientlogug_changelist"
    change_search_field_name = "screening_identifier"
    add_search_field_name = "screening_identifier"

    change_list_title = PatientLogUg._meta.verbose_name

    form = PatientLogUgForm

    fieldsets = (
        get_first_fieldset(),
        get_names_and_basic_demographics_fieldset(include_pii=False),
        get_contact_fieldset(),
        get_address_fielset(),
        get_health_fieldset(),
        get_health_talks_fieldset(),
        get_appointment_fieldset(),
        get_willingness_to_screen_fieldset(),
        get_screening_and_consent_fieldset(),
        get_group_fieldset(),
        audit_fieldset_tuple,
    )

    search_fields = get_search_fields(include_pii=False)

    @property
    def subject_screening_model_cls(self):
        return django_apps.get_model("intecomm_screening.subjectscreeningug")

    @property
    def subject_consent_model_cls(self):
        return django_apps.get_model("intecomm_consent.subjectconsentug")
