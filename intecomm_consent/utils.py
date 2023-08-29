from __future__ import annotations

from typing import TYPE_CHECKING, Type

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import format_html

from intecomm_screening.exceptions import AlreadyConsentedError

if TYPE_CHECKING:
    from intecomm_consent.models import SubjectConsent, SubjectConsentUg
    from intecomm_screening.models import SubjectScreening, SubjectScreeningUg


def raise_if_subject_consent_exists(
    screening_identifier: str | None = None,
    subject_screening: SubjectScreening | None = None,
    subject_screening_model_cls: Type[SubjectScreening | SubjectScreeningUg | None] = None,
    subject_consent_model_cls: Type[SubjectConsent | SubjectConsentUg | None] = None,
    is_modelform: bool | None = None,
) -> None:
    """Raises an exception if subject consent model instance exists."""
    screening_identifier = screening_identifier or subject_screening.screening_identifier
    try:
        subject_consent = subject_consent_model_cls.objects.get(
            screening_identifier=screening_identifier
        )
    except ObjectDoesNotExist:
        pass
    else:
        if is_modelform:
            if not subject_screening:
                subject_screening = subject_screening_model_cls.objects.get(
                    screening_identifier=screening_identifier
                )
            msg = format_html(
                "Not allowed. Subject has already consented. See subject {}.",
                subject_screening.subject_identifier,
            )
            raise forms.ValidationError(msg)

        else:
            raise AlreadyConsentedError(
                f"Subject has already consented. See {subject_consent.subject_identifier}. "
                f"Perhaps catch this in the form."
            )
