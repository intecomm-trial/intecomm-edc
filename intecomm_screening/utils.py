from __future__ import annotations

import re
from typing import TYPE_CHECKING

from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from edc_consent.utils import get_consent_model_cls
from edc_constants.constants import UUID_PATTERN
from edc_screening.utils import get_subject_screening_model_cls

if TYPE_CHECKING:
    from intecomm_consent.models import SubjectConsent
    from intecomm_screening.models import PatientLog, SubjectScreening


class AlreadyRefusedConsentError(Exception):
    pass


class InvalidScreeningIdentifier(Exception):
    pass


class InvalidSubjectIdentifier(Exception):
    pass


class MultipleConsentRefusalsDetectedError(Exception):
    pass


class ScreenedDespiteUnwillingToScreenError(Exception):
    pass


def get_consent_refusal_model_cls():
    return django_apps.get_model("intecomm_screening.consentrefusal")


def get_patient_log_model_cls():
    return django_apps.get_model("intecomm_screening.patientlog")


def get_subject_screening_url(
    patient_log: PatientLog,
    subject_screening: SubjectScreening | None = None,
    next_url_name: str | None = None,
) -> str | None:
    if subject_screening:
        url = subject_screening.get_absolute_url()
    else:
        absolute_url = get_subject_screening_model_cls()().get_absolute_url()
        url = f"{absolute_url}?patient_log_identifier={patient_log.patient_log_identifier}"
    if next_url_name:
        url = f"{url.split('?')[0]}?next={next_url_name}&{url.split('?')[1]}"
    return url


def get_subject_consent_url(
    subject_screening: SubjectScreening,
    subject_consent: SubjectConsent | None = None,
    next_url_name: str | None = None,
) -> str:
    """Returns an add url if subject is screened eligible or a change
    url if subject consent exists.
    """
    url = None
    try:
        subject_consent = subject_consent or get_consent_model_cls().objects.get(
            screening_identifier=subject_screening.screening_identifier
        )
    except ObjectDoesNotExist:
        if subject_screening and subject_screening.eligible:
            absolute_url = get_consent_model_cls()().get_absolute_url()
            url = (
                f"{absolute_url}?screening_identifier={subject_screening.screening_identifier}"
            )
    else:
        url = subject_consent.get_absolute_url()
    if next_url_name:
        url = f"{url.split('?')[0]}?next={next_url_name}&{url.split('?')[1]}"
    return url


def get_consent_refusal_url(
    screening_identifier: str,
    consent_refusal=None,
    next_url_name: str | None = None,
) -> str:
    get_consent_refusal_model_cls()
    try:
        consent_refusal = consent_refusal or get_consent_refusal_model_cls().objects.get(
            screening_identifier=screening_identifier
        )
    except ObjectDoesNotExist:
        url = get_consent_refusal_model_cls()().get_absolute_url()
        url = f"{url}?screening_identifier={screening_identifier}"
    else:
        url = consent_refusal.get_absolute_url()
    if next_url_name:
        url = f"{url.split('?')[0]}?next={next_url_name}&{url.split('?')[1]}"
    return url


def raise_if_consent_refusal_exists(
    screening_identifier: str, is_modelform: bool | None = None
) -> None:
    """Raises an exception if the consent refusal model instance
    exists.
    """
    try:
        get_consent_refusal_model_cls().objects.get(screening_identifier=screening_identifier)
    except ObjectDoesNotExist:
        pass
    else:
        if is_modelform:
            consent_refusal_url = get_consent_refusal_url(
                screening_identifier=screening_identifier
            )
            msg = format_html(
                "Not allowed. Patient has already refused consent. "
                'See subject <A href="{}">{}</A>',
                mark_safe(consent_refusal_url),  # nosec B308 B703
                screening_identifier,
            )
            raise forms.ValidationError(msg)

        else:
            raise AlreadyRefusedConsentError(
                f"Patient has already refused to consent. See {screening_identifier}. "
                "Perhaps catch this in the form."
            )


def validate_screening_identifier(screening_identifier: str, calling_model=None):
    """Raise if non-uuid identifier is not found in SubjectScreening."""
    if not screening_identifier or not re.match(UUID_PATTERN, screening_identifier):
        try:
            with transaction.atomic():
                get_subject_screening_model_cls().objects.get(
                    screening_identifier=screening_identifier
                )
        except ObjectDoesNotExist:
            raise InvalidScreeningIdentifier(
                f"Invalid screening identifier. See {calling_model._meta.verbose_name}. "
                f"Got `{screening_identifier}`. Perhaps catch this in the form."
            )


def validate_subject_identifier(subject_identifier, calling_model=None):
    """Raise if non-uuid identifier is not found in SubjectConsent."""
    if not subject_identifier or not re.match(UUID_PATTERN, subject_identifier):
        try:
            with transaction.atomic():
                get_consent_model_cls().objects.get(subject_identifier=subject_identifier)
        except ObjectDoesNotExist:
            raise InvalidSubjectIdentifier(
                f"Invalid subject identifier. See {calling_model._meta.verbose_name}. "
                f"Got `{subject_identifier}`. Perhaps catch this in the form."
            )
