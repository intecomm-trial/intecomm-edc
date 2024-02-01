from __future__ import annotations

from typing import TYPE_CHECKING

from django.apps import apps as django_apps
from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites import site_sites
from intecomm_rando.constants import TANZANIA

from ..admin_site import intecomm_consent_admin
from ..forms import SubjectConsentTzForm
from ..models import SubjectConsentTz
from .fieldsets import (
    get_first_fieldset,
    get_group_fieldset,
    get_review_questions_fieldset,
)
from .modeladmin_mixins import SubjectConsentModelAdminMixin

if TYPE_CHECKING:
    from django.db.models import QuerySet


__all__ = ["SubjectConsentTzAdmin"]


@admin.register(SubjectConsentTz, site=intecomm_consent_admin)
class SubjectConsentTzAdmin(
    SubjectConsentModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = SubjectConsentTzForm

    fieldsets = (
        get_first_fieldset(include_pii=True),
        get_review_questions_fieldset(),
        get_group_fieldset(),
        audit_fieldset_tuple,
    )

    search_fields = (
        "subject_identifier",
        "screening_identifier",
        "identity__exact",
        "initials__exact",
        "legal_name__exact",
        "familiar_name__exact",
    )

    @property
    def subject_screening_model_cls(self):
        return django_apps.get_model("intecomm_screening.subjectscreening")

    def get_queryset(self, request) -> QuerySet[SubjectConsentTz]:
        queryset = super().get_queryset(request)
        site_ids = [s.site_id for s in site_sites.get_by_country(TANZANIA, aslist=True)]
        return queryset.filter(site__in=site_ids)
