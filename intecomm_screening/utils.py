from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from django.apps import apps as django_apps
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.urls import reverse
from edc_consent.utils import get_consent_model_cls

if TYPE_CHECKING:
    from intecomm_screening.models import SubjectScreening


class AlreadyRefusedConsentError(Exception):
    pass


class MultipleConsentRefusalsDetectedError(Exception):
    pass


def get_add_or_change_consent_url(
    obj: SubjectScreening, next_url_name: str | None = None
) -> Tuple[str | None, str | None, str | None]:
    add_consent_url = None
    change_consent_url = None
    subject_identifier = None

    next_url_name = (
        next_url_name or "intecomm_screening_admin:intecomm_screening_patientlog_changelist"
    )

    try:
        subject_consent = get_consent_model_cls().objects.get(
            screening_identifier=obj.screening_identifier
        )
    except ObjectDoesNotExist:
        url = reverse("intecomm_consent_admin:intecomm_consent_subjectconsent_add")
        # TODO: remove sensitive data from url!!
        add_consent_url = (
            f"{url}?next={next_url_name}"
            f"&screening_identifier={obj.screening_identifier}"
            f"&identity={obj.hospital_identifier}"
            f"&initials={obj.initials}"
            f"&site={obj.site.id}"
            f"&gender={obj.gender}"
            f"&age_in_years={obj.age_in_years}"
            f"&legal_name={obj.legal_name}"
            f"&familiar_name={obj.familiar_name}"
        )
    else:
        subject_identifier = subject_consent.subject_identifier
        url = reverse(
            "intecomm_consent_admin:intecomm_consent_subjectconsent_change",
            args=(subject_consent.id,),
        )
        change_consent_url = f"{url}?next={next_url_name}"
    return add_consent_url, change_consent_url, subject_identifier


def get_consent_refusal_model_cls():
    return django_apps.get_model("intecomm_screening.consentrefusal")


def get_add_or_change_refusal_url(
    obj: SubjectScreening, next_url_name: str | None = None
) -> Tuple[str | None, str | None]:
    add_url = None
    change_url = None
    next_url_name = (
        next_url_name or "intecomm_screening_admin:intecomm_screening_patientlog_changelist"
    )

    try:
        consent_refusal = get_consent_refusal_model_cls().objects.get(
            screening_identifier=obj.screening_identifier
        )
    except ObjectDoesNotExist:
        url = reverse("intecomm_screening_admin:intecomm_screening_consentrefusal_add")
        add_url = f"{url}?next={next_url_name}&subject_screening={obj.id}"
    else:
        url = reverse(
            "intecomm_screening_admin:intecomm_screening_consentrefusal_change",
            args=(consent_refusal.id,),
        )
        change_url = f"{url}?next={next_url_name}"
    return add_url, change_url


def raise_if_already_refused_consent(screening_identifier: str):
    try:
        get_consent_refusal_model_cls().objects.get(screening_identifier=screening_identifier)
    except ObjectDoesNotExist:
        pass
    except MultipleObjectsReturned:
        raise MultipleConsentRefusalsDetectedError(
            f"Multiple consent refusals detected for {screening_identifier}. "
            "Perhaps catch this in the form."
        )
    else:
        raise AlreadyRefusedConsentError(
            f"Patient has already refused to consent. See {screening_identifier}. "
            "Perhaps catch this in the form."
        )
