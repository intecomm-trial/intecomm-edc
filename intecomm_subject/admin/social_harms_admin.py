from __future__ import annotations

from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..forms import SocialHarmsForm
from ..models import SocialHarms
from .modeladmin_mixins import CrfModelAdmin


def get_impact_fieldset(prefix: str, phrase: str, description: bool | None = None):
    fields = [f"{prefix}_impact"]
    if description:
        fields.append(f"{prefix}_impact_description")
    fields.extend(
        [
            f"{prefix}_impact_severity",
            f"{prefix}_impact_status",
            f"{prefix}_impact_help",
            f"{prefix}_impact_referal",
        ]
    )
    fields = tuple(fields)
    return (
        f"Impacts of participation on relationships: {prefix.upper()}",
        {
            "description": (
                f"Has participation in the study had a negative impact on {phrase}"
            ),
            "fields": fields,
        },
    )


@admin.register(SocialHarms, site=intecomm_subject_admin)
class SocialHarmsAdmin(CrfModelAdmin):
    form = SocialHarmsForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Disclosure",
            {
                "description": (
                    "Who knows about your participation in the study and how did "
                    "they find out?"
                ),
                "fields": (
                    "partner",
                    "partner_disclosure",
                    "family",
                    "family_disclosure",
                    "friends",
                    "friends_disclosure",
                    "coworkers",
                    "coworkers_disclosure",
                ),
            },
        ),
        get_impact_fieldset("partner", "your relationship with your partner"),
        get_impact_fieldset("family", "your relationship with your family"),
        get_impact_fieldset("friends", "your relationship with your friends"),
        get_impact_fieldset("coworkers", "your relationship with your co-workers"),
        get_impact_fieldset("healthcare", "your access to healthcare services"),
        get_impact_fieldset(
            "other_service", "your access to any other health services", description=True
        ),
        get_impact_fieldset("employment", "your employment"),
        get_impact_fieldset("insurance", "your health insurance"),
        get_impact_fieldset("other", "any other aspect of your life", description=True),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "partner": admin.VERTICAL,
        "partner_disclosure": admin.VERTICAL,
        "family": admin.VERTICAL,
        "family_disclosure": admin.VERTICAL,
        "friends": admin.VERTICAL,
        "friends_disclosure": admin.VERTICAL,
        "coworkers": admin.VERTICAL,
        "coworkers_disclosure": admin.VERTICAL,
        "partner_impact": admin.VERTICAL,
        "partner_impact_severity": admin.VERTICAL,
        "partner_impact_status": admin.VERTICAL,
        "partner_impact_help": admin.VERTICAL,
        "partner_impact_referal": admin.VERTICAL,
        "family_impact": admin.VERTICAL,
        "family_impact_severity": admin.VERTICAL,
        "family_impact_status": admin.VERTICAL,
        "family_impact_help": admin.VERTICAL,
        "family_impact_referal": admin.VERTICAL,
        "friends_impact": admin.VERTICAL,
        "friends_impact_severity": admin.VERTICAL,
        "friends_impact_status": admin.VERTICAL,
        "friends_impact_help": admin.VERTICAL,
        "friends_impact_referal": admin.VERTICAL,
        "coworkers_impact": admin.VERTICAL,
        "coworkers_impact_severity": admin.VERTICAL,
        "coworkers_impact_status": admin.VERTICAL,
        "coworkers_impact_help": admin.VERTICAL,
        "coworkers_impact_referal": admin.VERTICAL,
        "healthcare_impact": admin.VERTICAL,
        "healthcare_impact_severity": admin.VERTICAL,
        "healthcare_impact_status": admin.VERTICAL,
        "healthcare_impact_help": admin.VERTICAL,
        "healthcare_impact_referal": admin.VERTICAL,
        "other_service_impact": admin.VERTICAL,
        "other_service_impact_severity": admin.VERTICAL,
        "other_service_impact_status": admin.VERTICAL,
        "other_service_impact_help": admin.VERTICAL,
        "other_service_impact_referal": admin.VERTICAL,
        "employment_impact": admin.VERTICAL,
        "employment_impact_severity": admin.VERTICAL,
        "employment_impact_status": admin.VERTICAL,
        "employment_impact_help": admin.VERTICAL,
        "employment_impact_referal": admin.VERTICAL,
        "insurance_impact": admin.VERTICAL,
        "insurance_impact_severity": admin.VERTICAL,
        "insurance_impact_status": admin.VERTICAL,
        "insurance_impact_help": admin.VERTICAL,
        "insurance_impact_referal": admin.VERTICAL,
        "other_impact": admin.VERTICAL,
        "other_impact_severity": admin.VERTICAL,
        "other_impact_status": admin.VERTICAL,
        "other_impact_help": admin.VERTICAL,
        "other_impact_referal": admin.VERTICAL,
    }
