from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.mixins import ModelAdminRedirectAllToChangelistMixin
from edc_sites import site_sites
from intecomm_rando.constants import UGANDA

from intecomm_consent.models import SubjectConsentUg

from ...admin_site import intecomm_screening_admin
from ...forms import SubjectScreeningUgForm
from ...models import PatientLogUg, SubjectScreeningUg
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

if TYPE_CHECKING:
    from django.db.models import QuerySet


@admin.register(SubjectScreeningUg, site=intecomm_screening_admin)
class SubjectScreeningUgAdmin(
    SubjectScreeningModelAdminMixin,
    ModelAdminRedirectAllToChangelistMixin,
    BaseModelAdminMixin,
):
    form = SubjectScreeningUgForm
    ordering = ("site__id", "-report_datetime")

    # ModelAdminRedirectAllToChangelistMixin
    changelist_url = "intecomm_screening_admin:intecomm_screening_patientlogug_changelist"
    add_search_field_name = "patient_log_identifier"
    change_search_field_name = "screening_identifier"

    fieldsets = (
        get_first_fieldset(),
        get_demographics_fieldset(include_pii=False),
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
    )

    def patient_log_model_cls(self):
        return PatientLogUg

    def get_queryset(self, request) -> QuerySet[SubjectConsentUg]:
        queryset = super().get_queryset(request)
        site_ids = [s.site_id for s in site_sites.get_by_country(UGANDA, aslist=True)]
        return queryset.filter(site__in=site_ids)
