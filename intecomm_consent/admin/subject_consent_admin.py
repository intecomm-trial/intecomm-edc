from __future__ import annotations

from typing import Tuple

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django_audit_fields.admin import audit_fieldset_tuple
from edc_consent.actions import (
    flag_as_verified_against_paper,
    unflag_as_verified_against_paper,
)
from edc_consent.modeladmin_mixins import (
    ConsentModelAdminMixin,
    PiiNamesModelAdminMixin,
)
from edc_constants.choices import GENDER
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_model_admin.mixins import ModelAdminProtectPiiMixin
from edc_sites.admin import SiteModelAdminMixin

from intecomm_screening.admin.modeladmin_mixins import (
    InitialDataModelAdminMixin,
    RedirectAllToPatientLogModelAdminMixin,
)
from intecomm_screening.models import SubjectScreening
from intecomm_sites import all_sites

from ..admin_site import intecomm_consent_admin
from ..forms import SubjectConsentForm
from ..models import SubjectConsent


@admin.register(SubjectConsent, site=intecomm_consent_admin)
class SubjectConsentAdmin(
    PiiNamesModelAdminMixin,
    SiteModelAdminMixin,
    InitialDataModelAdminMixin,
    RedirectAllToPatientLogModelAdminMixin,
    ModelAdminProtectPiiMixin,
    ConsentModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = SubjectConsentForm

    name_fields: list[str] = ["legal_name", "familiar_name"]
    name_display_field: str = "familiar_name"
    all_sites = all_sites
    list_per_page = 5

    show_object_tools = False
    show_cancel = True
    change_list_template: str = "intecomm_consent/admin/subjectconsent_change_list.html"

    actions = [
        flag_as_verified_against_paper,
        unflag_as_verified_against_paper,
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "screening_identifier",
                    "subject_identifier",
                    "legal_name",
                    "familiar_name",
                    "initials",
                    "gender",
                    "language",
                    "is_literate",
                    "witness_name",
                    "consent_datetime",
                    "dob",
                    "is_dob_estimated",
                    "identity",
                    "identity_type",
                    "confirm_identity",
                    "is_incarcerated",
                )
            },
        ),
        (
            "Review Questions",
            {
                "fields": (
                    "consent_reviewed",
                    "study_questions",
                    "assessment_score",
                    "consent_signature",
                    "consent_copy",
                ),
                "description": "The following questions are directed to the interviewer.",
            },
        ),
        (
            "Group",
            {"classes": ("collapse",), "fields": ("group_identifier",)},
        ),
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

    radio_fields = {
        "gender": admin.VERTICAL,
        "assessment_score": admin.VERTICAL,
        "consent_copy": admin.VERTICAL,
        "consent_reviewed": admin.VERTICAL,
        "consent_signature": admin.VERTICAL,
        "is_dob_estimated": admin.VERTICAL,
        "identity_type": admin.VERTICAL,
        "is_incarcerated": admin.VERTICAL,
        "is_literate": admin.VERTICAL,
        "language": admin.VERTICAL,
        "study_questions": admin.VERTICAL,
    }

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "gender":
            kwargs["choices"] = GENDER
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None) -> Tuple[str, ...]:
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if "group_identifier" not in readonly_fields:
            readonly_fields += ("group_identifier",)
        return readonly_fields

    def get_changeform_initial_data(self, request) -> dict:
        dct = super().get_changeform_initial_data(request)
        try:
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=dct.get("screening_identifier")
            )
        except ObjectDoesNotExist:
            pass
        else:
            dct.update(**self.initial_form_data(request, subject_screening))
        return dct
