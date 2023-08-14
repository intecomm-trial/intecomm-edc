from __future__ import annotations

import re
from typing import Tuple

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import format_html
from django_audit_fields import audit_fieldset_tuple
from edc_consent.modeladmin_mixins import PiiNamesModelAdminMixin
from edc_constants.choices import GENDER
from edc_constants.constants import UUID_PATTERN
from edc_model_admin.mixins import ModelAdminHideDeleteButtonOnCondition
from edc_screening.utils import format_reasons_ineligible
from edc_sites.admin import SiteModelAdminMixin

from intecomm_sites import all_sites

from ..admin_site import intecomm_screening_admin
from ..forms import SubjectScreeningForm
from ..models import PatientLog, SubjectScreening
from ..utils import get_consent_refusal_model_cls
from .modeladmin_mixins import (
    BaseModelAdminMixin,
    InitialDataModelAdminMixin,
    RedirectAllToPatientLogModelAdminMixin,
)


@admin.register(SubjectScreening, site=intecomm_screening_admin)
class SubjectScreeningAdmin(
    PiiNamesModelAdminMixin,
    SiteModelAdminMixin,
    InitialDataModelAdminMixin,
    RedirectAllToPatientLogModelAdminMixin,
    ModelAdminHideDeleteButtonOnCondition,
    BaseModelAdminMixin,
):
    form = SubjectScreeningForm
    list_per_page = 5
    autocomplete_fields = ["site"]
    show_object_tools = True
    show_cancel = True
    change_list_template: str = "intecomm_screening/admin/subjectscreening_change_list.html"

    # PiiNamesModelAdminMixin attrs
    name_fields: list[str] = ["legal_name", "familiar_name"]
    name_display_field: str = "familiar_name"
    all_sites: dict = all_sites

    # RedirectAllToPatientLogModelAdminMixin attr
    add_search_field_name = "patient_log_identifier"
    change_search_field_name = "screening_identifier"

    additional_instructions = (
        "Patients must meet ALL of the inclusion criteria and NONE of the "
        "exclusion criteria in order to proceed to the final screening stage"
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "report_datetime",
                    "site",
                    "patient_log_identifier",
                )
            },
        ),
        (
            "Demographics",
            {
                "description": (
                    "Please review carefully. If anything needs to be changed, do so on "
                    "the Patient Log and try again"
                ),
                "fields": (
                    "legal_name",
                    "familiar_name",
                    "initials",
                    "hospital_identifier",
                    "gender",
                    "age_in_years",
                ),
            },
        ),
        (
            "Health facility",
            {
                "fields": (
                    "in_care_6m",
                    "in_care_duration",
                )
            },
        ),
        (
            "HIV",
            {
                "fields": (
                    "hiv_dx",
                    "hiv_dx_6m",
                    "hiv_dx_ago",
                    "art_unchanged_3m",
                    "art_stable",
                    "art_adherent",
                )
            },
        ),
        (
            "Diabetes",
            {
                "fields": (
                    "dm_dx",
                    "dm_dx_6m",
                    "dm_dx_ago",
                    "dm_complications",
                )
            },
        ),
        (
            "Hypertension",
            {
                "fields": (
                    "htn_dx",
                    "htn_dx_6m",
                    "htn_dx_ago",
                    "htn_complications",
                )
            },
        ),
        (
            "Pregnancy",
            {"fields": ("pregnant",)},
        ),
        (
            "Other history",
            {
                "fields": (
                    "excluded_by_bp_history",
                    "excluded_by_gluc_history",
                    "requires_acute_care",
                )
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "lives_nearby",
                    "staying_nearby_6",
                )
            },
        ),
        (
            "Blood pressure measurements",
            {
                "fields": (
                    "sys_blood_pressure_one",
                    "dia_blood_pressure_one",
                    "sys_blood_pressure_two",
                    "dia_blood_pressure_two",
                )
            },
        ),
        (
            "Other",
            {
                "fields": (
                    "consent_ability",
                    "unsuitable_for_study",
                    "reasons_unsuitable",
                    "unsuitable_agreed",
                )
            },
        ),
        (
            "Updates",
            {
                "classes": ("collapse",),
                "fields": (
                    "screening_identifier",
                    "eligible",
                    "eligibility_datetime",
                    "real_eligibility_datetime",
                    "reasons_ineligible",
                    "subject_identifier",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "screening_identifier",
        "eligibility_status",
        "demographics",
        "reasons",
        "report_datetime",
        "user_created",
        "created",
        "site_code",
    )

    list_filter = (
        "report_datetime",
        "gender",
        "eligible",
        "consented",
        "refused",
    )

    search_fields = (
        "screening_identifier",
        "subject_identifier",
        "hospital_identifier__exact",
        "initials__exact",
        "reasons_ineligible",
        "legal_name__exact",
        "familiar_name__exact",
    )

    readonly_fields = (
        "screening_identifier",
        "eligible",
        "eligibility_datetime",
        "real_eligibility_datetime",
        "reasons_ineligible",
        "subject_identifier",
    )

    radio_fields = {
        "art_adherent": admin.VERTICAL,
        "art_stable": admin.VERTICAL,
        "art_unchanged_3m": admin.VERTICAL,
        "consent_ability": admin.VERTICAL,
        "dm_complications": admin.VERTICAL,
        "dm_dx": admin.VERTICAL,
        "dm_dx_6m": admin.VERTICAL,
        "excluded_by_bp_history": admin.VERTICAL,
        "excluded_by_gluc_history": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "hiv_dx": admin.VERTICAL,
        "hiv_dx_6m": admin.VERTICAL,
        "htn_complications": admin.VERTICAL,
        "htn_dx": admin.VERTICAL,
        "htn_dx_6m": admin.VERTICAL,
        "in_care_6m": admin.VERTICAL,
        "lives_nearby": admin.VERTICAL,
        "pregnant": admin.VERTICAL,
        "requires_acute_care": admin.VERTICAL,
        "selection_method": admin.VERTICAL,
        "staying_nearby_6": admin.VERTICAL,
        "unsuitable_agreed": admin.VERTICAL,
        "unsuitable_for_study": admin.VERTICAL,
    }

    def post_url_on_delete_kwargs(self, request, obj):
        return {}

    def get_readonly_fields(self, request, obj=None) -> Tuple[str, ...]:
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj:
            readonly_fields = readonly_fields + ("patient_log",)
        return readonly_fields

    @staticmethod
    @admin.display(description="Eligibile", ordering="eligible")
    def eligibility_status(obj=None):
        return format_html('<span style="color:green;">YES</span>' if obj.eligible else "NO")

    @staticmethod
    def demographics(obj=None):
        data = [
            f"{obj.get_gender_display()} {obj.age_in_years}yrs",
            f"Initials: {obj.initials.upper()}<BR>",
            f"Hospital ID: {obj.hospital_identifier}",
        ]
        return format_html("<BR>".join(data))

    def reasons(self, obj=None):
        if not obj.reasons_ineligible:
            return self.dashboard(obj)
        return format_reasons_ineligible(obj.reasons_ineligible)

    def hide_delete_button_on_condition(self, request, object_id) -> bool:
        """Hide delete button on form if subject identifier not
        set or consent_refusal exists.
        """
        obj = self.model.objects.get(id=object_id)
        try:
            consent_refusal = get_consent_refusal_model_cls().objects.get(
                screening_identifier=obj.screening_identifier
            )
        except ObjectDoesNotExist:
            consent_refusal = None
        if not re.match(UUID_PATTERN, obj.subject_identifier) or consent_refusal:
            return True
        return super().hide_delete_button_on_condition(request, object_id)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "gender":
            kwargs["choices"] = GENDER
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def get_changeform_initial_data(self, request) -> dict:
        dct = super().get_changeform_initial_data(request)
        try:
            patient_log = PatientLog.objects.get(
                patient_log_identifier=dct.get("patient_log_identifier")
            )
        except ObjectDoesNotExist:
            pass
        else:
            dct.update(**self.initial_form_data(request, patient_log))
        return dct
