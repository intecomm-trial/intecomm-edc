from bs4 import BeautifulSoup
from django import template
from edc_constants.constants import NO, TBD, YES
from edc_dashboard.url_names import url_names
from edc_dashboard.utils import get_bootstrap_version
from edc_screening.constants import ELIGIBLE, NOT_ELIGIBLE

register = template.Library()


@register.inclusion_tag(
    f"intecomm_dashboard/bootstrap{get_bootstrap_version()}/" f"buttons/screening_button.html",
    takes_context=True,
)
def screening_button(context, model_wrapper):
    title = "Edit subject's screening form"
    perms = context["perms"]
    enabled = perms.user.has_perm(
        "intecomm_screening.view_subjectscreening"
    ) or perms.user.has_perm("intecomm_screening.change_subjectscreening")
    return dict(
        perms=context["perms"],
        screening_identifier=model_wrapper.object.screening_identifier,
        enabled=enabled,
        title=title,
        YES=YES,
        NO=NO,
        TBD=TBD,
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
    )


def refusal_button(context, subject_refusal_model_wrapper):
    title = ["Capture subject's primary reason for not joining."]

    return dict(
        perms=context["perms"],
        href=subject_refusal_model_wrapper.href,
        title=" ".join(title),
    )


@register.inclusion_tag(
    f"intecomm_dashboard/bootstrap{get_bootstrap_version()}/" f"buttons/dashboard_button.html"
)
def dashboard_button(model_wrapper):
    subject_dashboard_url = url_names.get("subject_dashboard_url")
    return dict(
        subject_dashboard_url=subject_dashboard_url,
        subject_identifier=model_wrapper.subject_identifier,
    )