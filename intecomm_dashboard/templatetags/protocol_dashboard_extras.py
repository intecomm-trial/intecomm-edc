from __future__ import annotations

from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from edc_constants.constants import NO, TBD, YES
from edc_dashboard.url_names import url_names
from edc_dashboard.utils import get_bootstrap_version
from edc_screening.constants import ELIGIBLE, NOT_ELIGIBLE
from edc_sites.site import sites
from intecomm_rando.constants import UGANDA

from intecomm_screening.models import PatientLog
from intecomm_screening.utils import get_consent_refusal_url, get_subject_consent_url

if TYPE_CHECKING:
    pass


register = template.Library()


@register.inclusion_tag(
    f"intecomm_dashboard/bootstrap{get_bootstrap_version()}/" f"buttons/screening_button.html",
    takes_context=True,
)
def screening_button(context, model_wrapper):
    title = "Edit subject's screening form"
    perms = context["perms"]
    if model_wrapper.object.eligible is False:
        eligible = NO
    elif model_wrapper.object.eligible is True:
        eligible = YES
    else:
        eligible = TBD
    enabled = perms.user.has_perm(
        "intecomm_screening.view_subjectscreening"
    ) or perms.user.has_perm("intecomm_screening.change_subjectscreening")
    return dict(
        perms=context["perms"],
        screening_identifier=model_wrapper.object.screening_identifier,
        enabled=enabled,
        eligible=eligible,
        title=title,
        YES=YES,
        NO=NO,
        TBD=TBD,
        href=model_wrapper.href,
    )


@register.inclusion_tag(
    f"intecomm_dashboard/bootstrap{get_bootstrap_version()}/"
    f"buttons/eligibility_button.html"
)
def eligibility_button(subject_screening_model_wrapper):
    comment = []
    obj = subject_screening_model_wrapper.object
    tooltip = None
    if obj.reasons_ineligible:
        comment = obj.reasons_ineligible.split("|")
        comment = list(set(comment))
        comment.sort()
    display_label = ELIGIBLE if obj.eligible else NOT_ELIGIBLE
    soup = BeautifulSoup(display_label, features="html.parser")
    return dict(
        eligible=obj.eligible,
        eligible_final=obj.eligible,
        display_label=soup.get_text(),
        comment=comment,
        tooltip=tooltip,
        TBD=TBD,
    )


@register.inclusion_tag(
    f"intecomm_dashboard/bootstrap{get_bootstrap_version()}/buttons/add_consent_button.html",
    takes_context=True,
)
def add_consent_button(context, model_wrapper):
    title = ["Consent subject to participate."]
    consent_version = model_wrapper.consent.version
    url = get_subject_consent_url(
        subject_screening=model_wrapper.object,
        next_url_name="intecomm_dashboard:screening_listboard_url,screening_identifier",
    )
    return dict(
        perms=context["perms"],
        screening_identifier=model_wrapper.object.screening_identifier,
        href=model_wrapper.consent.href,
        consent_version=consent_version,
        title=" ".join(title),
        add_consent_url=url,
        change_consent_url=url,
        subject_identifier=model_wrapper.object.subject_identifier,
    )


@register.inclusion_tag(
    f"intecomm_dashboard/bootstrap{get_bootstrap_version()}/"
    f"buttons/patient_log_button.html",
    takes_context=True,
)
def patient_log_button(context, model_wrapper):
    change_list_href = None
    title = "Go to patient's log"
    screening_identifier = model_wrapper.object.screening_identifier
    try:
        obj = PatientLog.objects.get(screening_identifier=screening_identifier)
    except ObjectDoesNotExist:
        pass
    else:
        if sites.get_current_country(context["request"]) == UGANDA:
            change_list_href = reverse(
                "intecomm_screening_admin:intecomm_screening_patientlogug_changelist"
            )
        else:
            change_list_href = reverse(
                "intecomm_screening_admin:intecomm_screening_patientlog_changelist"
            )

        change_list_href = f"{change_list_href}?q={obj.id}"
    return dict(
        perms=context["perms"],
        change_list_href=change_list_href,
        title=title,
    )


@register.inclusion_tag(
    f"intecomm_dashboard/bootstrap{get_bootstrap_version()}/"
    f"buttons/patient_group_button.html",
    takes_context=True,
)
def patient_group_button(context, model_wrapper):
    change_list_href = None
    patient_group = None
    title = "Go to patient's group"
    screening_identifier = model_wrapper.object.screening_identifier
    try:
        obj = PatientLog.objects.get(screening_identifier=screening_identifier)
    except ObjectDoesNotExist:
        pass
    else:
        if patient_group := obj.patientgroup_set.all().first():
            change_list_href = reverse(
                "intecomm_screening_admin:intecomm_screening_patientgroup_changelist"
            )
            change_list_href = f"{change_list_href}?q={patient_group.name}"
    return dict(
        perms=context["perms"],
        change_list_href=change_list_href,
        title=title,
        patient_group=patient_group,
    )


@register.inclusion_tag(
    f"intecomm_dashboard/bootstrap{get_bootstrap_version()}/" f"buttons/refusal_button.html",
    takes_context=True,
)
def refusal_button(context, model_wrapper):
    title = ["Capture patient's primary reason for not consenting."]
    subject_screening = model_wrapper.object
    url = get_consent_refusal_url(screening_identifier=subject_screening.screening_identifier)

    return dict(
        perms=context["perms"],
        href=url,
        title=" ".join(title),
    )


@register.inclusion_tag(
    f"intecomm_dashboard/bootstrap{get_bootstrap_version()}/buttons/dashboard_button.html"
)
def dashboard_button(model_wrapper):
    subject_dashboard_url = url_names.get("subject_dashboard_url")
    subject_dashboard_href = reverse(
        subject_dashboard_url, args=(model_wrapper.subject_identifier,)
    )
    title = "Go to subject's dashboard"
    return dict(
        subject_dashboard_href=subject_dashboard_href,
        subject_identifier=model_wrapper.subject_identifier,
        title=title,
    )


@register.inclusion_tag(
    f"intecomm_dashboard/bootstrap{get_bootstrap_version()}/changelist_topbar.html",
    takes_context=True,
)
def intecomm_changelist_topbar(context, selected: str):
    context["selected"] = selected
    if sites.get_current_country(context["request"]) == UGANDA:
        patient_log_changelist_url = (
            "intecomm_screening_admin:intecomm_screening_patientlogug_changelist"
        )
    else:
        patient_log_changelist_url = (
            "intecomm_screening_admin:intecomm_screening_patientlog_changelist"
        )
    context["patient_log_changelist_url"] = reverse(patient_log_changelist_url)
    return context
