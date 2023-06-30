from __future__ import annotations

import re
from typing import TYPE_CHECKING, Tuple

from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import transaction
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from edc_consent.utils import get_consent_model_cls
from edc_constants.constants import DM, HIV, HTN, UUID_PATTERN
from edc_dashboard.url_names import url_names
from edc_screening.utils import get_subject_screening_model_cls

if TYPE_CHECKING:
    from intecomm_screening.models import ConsentRefusal, SubjectScreening


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


def get_patient_log_model_cls():
    return django_apps.get_model("intecomm_screening.patientlog")


def get_consent_refusal_url(
    consent_refusal: ConsentRefusal | None = None,
    subject_screening: SubjectScreening | None = None,
    next_url_name: str | None = None,
) -> str | None:
    next_url_name = (
        next_url_name or "intecomm_screening_admin:intecomm_screening_patientlog_changelist"
    )
    if not consent_refusal:
        url = reverse("intecomm_screening_admin:intecomm_screening_consentrefusal_add")
        url = f"{url}?next={next_url_name}&subject_screening={subject_screening.id}"
    else:
        url = reverse(
            "intecomm_screening_admin:intecomm_screening_consentrefusal_change",
            args=(consent_refusal.id,),
        )
        url = f"{url}?next={next_url_name}"
    return url


def raise_if_screened_despite_unwilling_to_screen(patient_log) -> None:
    if patient_log.screening_refusal_reason:
        raise ScreenedDespiteUnwillingToScreenError(
            f"Patient '{patient_log.patient_log_identifier}' "
            f"has screened ({patient_log.screening_identifier}) "
            "despite reporting as unwilling to screen. "
            "Perhaps catch this in the form. "
            f"Got reason '{patient_log.screening_refusal_reason}'"
        )


def raise_if_consent_refusal_exists(
    screening_identifier: str, is_modelform: bool | None = None
) -> None:
    """Raises an exception if the consent refusal model instance
    exists.
    """
    try:
        consent_refusal = get_consent_refusal_model_cls().objects.get(
            screening_identifier=screening_identifier
        )
    except ObjectDoesNotExist:
        pass
    else:
        if is_modelform:
            consent_refusal_url = get_consent_refusal_url(consent_refusal=consent_refusal)
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


def raise_if_not_eligible(subject_screening: SubjectScreening) -> None:
    if not subject_screening.eligible:
        url_name = url_names.get("screening_listboard_url")
        url = reverse(
            url_name,
            kwargs={"screening_identifier": subject_screening.screening_identifier},
        )
        msg = format_html(
            'Not allowed. Subject is not eligible. See subject <A href="{}">{}</A>',
            mark_safe(url),  # nosec B308 B703
            subject_screening.screening_identifier,
        )
        raise forms.ValidationError(msg)


def validate_not_screened_despite_unwilling_to_screen(
    subject_screening: SubjectScreening,
) -> None:
    try:
        raise_if_screened_despite_unwilling_to_screen(
            screening_identifier=subject_screening.screening_identifier
        )
    except ScreenedDespiteUnwillingToScreenError:
        patient_log_identifier = None
        try:
            patient_log_identifier = (
                get_patient_log_model_cls()
                .objects.get(screening_identifier=subject_screening.screening_identifier)
                .patient_log_identifier
            )
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            pass

        raise forms.ValidationError(
            f"Not allowed. Patient '{patient_log_identifier}' "
            f"has screened ({subject_screening.screening_identifier}) "
            "despite reporting as unwilling to screen. "
            "Inform data manager before continuing.",
        )
    except ObjectDoesNotExist:
        raise forms.ValidationError(
            f"Invalid. Patient Log associated with screening identifier "
            f"'{subject_screening.screening_identifier}' not found"
        )
    except MultipleObjectsReturned:
        raise forms.ValidationError(
            f"Invalid. Multiple Patient Logs associated with screening identifier "
            f"'{subject_screening.screening_identifier}' exist."
            "Inform data manager before continuing.",
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


def abbrev_cond(c: list | None) -> str:
    c = sorted(c, key=str.casefold)
    if c == [DM]:
        abbrev = "*d*"
    elif c == [DM, HIV]:
        abbrev = "hd*"
    elif c == [DM, HTN]:
        abbrev = "*dt"
    elif c == [DM, HIV, HTN]:
        abbrev = "hdt"
    elif c == [HIV]:
        abbrev = "h**"
    elif c == [HIV, HTN]:
        abbrev = "h*t"
    elif c == [HTN]:
        abbrev = "**t"
    elif not c:
        abbrev = "***"
    else:
        raise TypeError(f"Invalid list of conditions. Got c == {c}.")
    return abbrev
