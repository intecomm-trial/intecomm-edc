from __future__ import annotations

from typing import TYPE_CHECKING

from django import forms
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from edc_consent.utils import get_consent_model_cls

from intecomm_screening.utils import get_add_or_change_consent_url

if TYPE_CHECKING:
    from intecomm_screening.models import SubjectScreening


class AlreadyConsentedError(Exception):
    pass


class MultipleConsentsDetectedError(Exception):
    pass


def raise_if_already_consented(screening_identifier: str):
    try:
        subject_consent = get_consent_model_cls().objects.get(
            screening_identifier=screening_identifier
        )
    except ObjectDoesNotExist:
        pass
    except MultipleObjectsReturned:
        raise MultipleConsentsDetectedError(
            f"Multiple subject consents detected for {screening_identifier}. "
            f"Perhaps catch this in the form."
        )
    else:
        raise AlreadyConsentedError(
            f"Subject has already consented. See {subject_consent.subject_identifier}. "
            f"Perhaps catch this in the form."
        )


def validate_not_already_consented(subject_screening: SubjectScreening) -> None:
    try:
        raise_if_already_consented(screening_identifier=subject_screening.screening_identifier)
    except AlreadyConsentedError:
        _, consent_url, subject_identifier = get_add_or_change_consent_url(
            obj=subject_screening
        )
        msg = format_html(
            'Not allowed. Subject has already consented. See subject <A href="{}">{}</A>',
            mark_safe(consent_url),  # nosec B308 B703
            subject_identifier,
        )
        raise forms.ValidationError(msg)
    except MultipleConsentsDetectedError:
        raise forms.ValidationError(
            "Not allowed. Multiple subject consents detected "
            f"for subject '{subject_screening.screening_identifier}'. "
            "Inform data manager before continuing."
        )
