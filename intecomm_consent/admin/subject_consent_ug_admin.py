from __future__ import annotations

from django.apps import apps as django_apps
from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.history import SimpleHistoryAdmin

from intecomm_sites import all_sites

from ..admin_site import intecomm_consent_admin
from ..models import SubjectConsentUg
from .fieldsets import (
    get_first_fieldset,
    get_group_fieldset,
    get_review_questions_fieldset,
)
from .modeladmin_mixins import SubjectConsentModelAdminMixin


@admin.register(SubjectConsentUg, site=intecomm_consent_admin)
class SubjectConsentUgAdmin(
    SubjectConsentModelAdminMixin,
    SimpleHistoryAdmin,
):
    all_sites = all_sites

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
