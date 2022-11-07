from bs4 import BeautifulSoup
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from edc_constants.constants import NO, TBD, YES
from edc_dashboard.url_names import url_names
from edc_dashboard.utils import get_bootstrap_version
from edc_screening.constants import ELIGIBLE, NOT_ELIGIBLE

from intecomm_screening.models import PatientLog, SubjectRefusal

from ..model_wrappers import SubjectRefusalModelWrapper

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
    return dict(
        perms=context["perms"],
        screening_identifier=model_wrapper.object.screening_identifier,
        href=model_wrapper.consent.href,
        consent_version=consent_version,
        title=" ".join(title),
        change_list_url=reverse(
            "intecomm_consent_admin:intecomm_consent_subjectconsent_changelist"
        ),
    )


@register.inclusion_tag(
    f"intecomm_dashboard/bootstrap{get_bootstrap_version()}/"
    f"buttons/patient_group_button.html",
    takes_context=True,
)
def patient_group_button(context, model_wrapper):
    change_list_href = None
    patient_group_name = None
    title = "Go to patient's group"
    screening_identifier = model_wrapper.object.screening_identifier
    try:
        obj = PatientLog.objects.get(screening_identifier=screening_identifier)
    except ObjectDoesNotExist:
        pass
    else:
        if obj.patient_group:
            patient_group_name = obj.patient_group.name
            change_list_href = reverse(
                "intecomm_screening_admin:intecomm_screening_patientgroup_changelist"
            )
            change_list_href = f"{change_list_href}?q={patient_group_name}"
    return dict(
        perms=context["perms"],
        change_list_href=change_list_href,
        title=title,
        patient_group_name=patient_group_name,
    )


@register.inclusion_tag(
    f"intecomm_dashboard/bootstrap{get_bootstrap_version()}/" f"buttons/refusal_button.html",
    takes_context=True,
)
def refusal_button(context, model_wrapper):
    title = ["Capture patient's primary reason for not consenting."]
    screening_identifier = model_wrapper.object.screening_identifier
    try:
        obj = SubjectRefusal.objects.get(screening_identifier=screening_identifier)
    except ObjectDoesNotExist:
        obj = SubjectRefusal()
    model_wrapper = SubjectRefusalModelWrapper(model_obj=obj)
    return dict(
        perms=context["perms"],
        href=model_wrapper.href,
        title=" ".join(title),
    )


@register.inclusion_tag(
    f"intecomm_dashboard/bootstrap{get_bootstrap_version()}/buttons/dashboard_button.html"
)
def dashboard_button(model_wrapper):
    subject_dashboard_url = url_names.get("subject_dashboard_url")
    # get randomized
    if not model_wrapper.object.patient_log.patient_group:
        randomized = False
    else:
        randomized = model_wrapper.object.patient_log.patient_group.randomized
    subject_dashboard_href = "#"
    if randomized:
        subject_dashboard_href = reverse(
            subject_dashboard_url, args=(model_wrapper.subject_identifier,)
        )
    title = "Go to subject's dashboard"
    if not randomized:
        title = "(Disabled) Subject's group has not randomized."
    return dict(
        subject_dashboard_href=subject_dashboard_href,
        subject_identifier=model_wrapper.subject_identifier,
        randomized=randomized,
        title=title,
    )
