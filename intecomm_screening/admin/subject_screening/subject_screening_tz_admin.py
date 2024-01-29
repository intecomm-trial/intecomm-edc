from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.mixins import ModelAdminRedirectAllToChangelistMixin
from edc_sites import site_sites
from intecomm_rando.constants import TANZANIA

from ...admin_site import intecomm_screening_admin
from ...forms import SubjectScreeningForm
from ...models import PatientLog, SubjectScreeningTz
from ..modeladmin_mixins import BaseModelAdminMixin
from .fieldsets import (
    get_bp_fieldset,
    get_demographics_fieldset,
    get_dm_fieldset,
    get_first_fieldset,
    get_health_facility_fieldset,
    get_hiv_fieldset,
    get_htn_fieldset,
    get_location_fieldset,
    get_other_fieldset,
    get_other_history_fieldset,
    get_pregnancy_fieldset,
    get_updates_fieldset,
)
from .modeladmin_mixins import SubjectScreeningModelAdminMixin


@admin.register(SubjectScreeningTz, site=intecomm_screening_admin)
class SubjectScreeningTzAdmin(
    SubjectScreeningModelAdminMixin,
    ModelAdminRedirectAllToChangelistMixin,
    BaseModelAdminMixin,
):
    form = SubjectScreeningForm
    ordering = ("site__id", "-report_datetime")

    # ModelAdminRedirectAllToChangelistMixin
    changelist_url = "intecomm_screening_admin:intecomm_screening_patientlog_changelist"
    add_search_field_name = "patient_log_identifier"
    change_search_field_name = "screening_identifier"

    fieldsets = (
        get_first_fieldset(),
        get_demographics_fieldset(include_pii=True),
        get_health_facility_fieldset(),
        get_hiv_fieldset(),
        get_dm_fieldset(),
        get_htn_fieldset(),
        get_pregnancy_fieldset(),
        get_other_history_fieldset(),
        get_location_fieldset(),
        get_bp_fieldset(),
        get_other_fieldset(),
        get_updates_fieldset(),
        audit_fieldset_tuple,
    )

    search_fields = (
        "patient_log_identifier",
        "screening_identifier",
        "subject_identifier",
        "hospital_identifier__exact",
        "initials__exact",
        "reasons_ineligible",
        "legal_name__exact",
        "familiar_name__exact",
    )

    def patient_log_model_cls(self):
        return PatientLog

    def get_queryset(self, request) -> QuerySet[SubjectScreeningTz]:
        queryset = super().get_queryset(request)
        site_ids = [s.site_id for s in site_sites.get_by_country(TANZANIA, aslist=True)]
        return queryset.filter(site__in=site_ids)
