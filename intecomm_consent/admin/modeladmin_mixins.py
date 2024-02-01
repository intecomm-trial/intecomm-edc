from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Type

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from edc_consent.actions import (
    flag_as_verified_against_paper,
    unflag_as_verified_against_paper,
)
from edc_consent.modeladmin_mixins import ConsentModelAdminMixin
from edc_constants.choices import GENDER
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_sites.admin import SiteModelAdminMixin

from intecomm_screening.admin.modeladmin_mixins import (
    InitialDataModelAdminMixin,
    RedirectAllToPatientLogModelAdminMixin,
)

if TYPE_CHECKING:
    from intecomm_screening.models import SubjectScreeningTz, SubjectScreeningUg


class SubjectConsentModelAdminMixin(
    SiteModelAdminMixin,
    InitialDataModelAdminMixin,
    RedirectAllToPatientLogModelAdminMixin,
    ConsentModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
):
    list_per_page = 5

    show_object_tools = False
    show_cancel = True
    change_list_template: str = "intecomm_consent/admin/subjectconsent_change_list.html"
    name_fields: list[str] = ["legal_name", "familiar_name"]
    name_display_field: str = "familiar_name"

    actions = [
        flag_as_verified_against_paper,
        unflag_as_verified_against_paper,
    ]

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

    @property
    def subject_screening_model_cls(self) -> Type[SubjectScreeningTz, SubjectScreeningUg]:
        pass

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
            subject_screening = self.subject_screening_model_cls.objects.get(
                screening_identifier=dct.get("screening_identifier")
            )
        except ObjectDoesNotExist:
            pass
        else:
            dct.update(**self.initial_form_data(request, subject_screening))
            try:
                identity = dct["hospital_identifier"]
            except KeyError:
                pass
            else:
                dct["identity"] = identity
        return dct
