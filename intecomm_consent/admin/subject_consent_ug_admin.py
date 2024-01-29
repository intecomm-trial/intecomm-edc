from __future__ import annotations

from typing import TYPE_CHECKING

from django.apps import apps as django_apps
from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites import site_sites
from intecomm_rando.constants import UGANDA

from ..admin_site import intecomm_consent_admin
from ..forms import SubjectConsentUgForm
from ..models import SubjectConsentUg
from .fieldsets import (
    get_first_fieldset,
    get_group_fieldset,
    get_review_questions_fieldset,
)
from .modeladmin_mixins import SubjectConsentModelAdminMixin

if TYPE_CHECKING:
    from django.db.models import QuerySet

__all__ = ["SubjectConsentUgAdmin"]


@admin.register(SubjectConsentUg, site=intecomm_consent_admin)
class SubjectConsentUgAdmin(
    SubjectConsentModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = SubjectConsentUgForm

    # ModelAdminRedirectAllToChangelistMixin
    changelist_url = "intecomm_screening_admin:intecomm_screening_patientlogug_changelist"
    change_search_field_name = "screening_identifier"
    add_search_field_name = "screening_identifier"

    fieldsets = (
        get_first_fieldset(include_pii=False),
        get_review_questions_fieldset(),
        get_group_fieldset(),
        audit_fieldset_tuple,
    )

    search_fields = (
        "subject_identifier",
        "screening_identifier",
        "identity__exact",
        "initials__exact",
    )

    @property
    def subject_screening_model_cls(self):
        return django_apps.get_model("intecomm_screening.subjectscreeningug")

    def get_queryset(self, request) -> QuerySet[SubjectConsentUg]:
        queryset = super().get_queryset(request)
        site_ids = [s.site_id for s in site_sites.get_by_country(UGANDA, aslist=True)]
        return queryset.filter(site__in=site_ids)
