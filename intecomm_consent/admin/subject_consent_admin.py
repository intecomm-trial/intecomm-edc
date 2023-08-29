from __future__ import annotations

from django.apps import apps as django_apps
from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import intecomm_consent_admin
from ..models import SubjectConsent
from .fieldsets import (
    get_first_fieldset,
    get_group_fieldset,
    get_review_questions_fieldset,
)
from .modeladmin_mixins import SubjectConsentModelAdminMixin


@admin.register(SubjectConsent, site=intecomm_consent_admin)
class SubjectConsentAdmin(SubjectConsentModelAdminMixin, SimpleHistoryAdmin):
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
