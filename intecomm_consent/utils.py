from __future__ import annotations

from typing import TYPE_CHECKING

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from edc_consent.utils import get_consent_model_cls
from edc_screening.utils import get_subject_screening_model_cls

from intecomm_screening.exceptions import AlreadyConsentedError
from intecomm_screening.utils import get_subject_consent_url

if TYPE_CHECKING:
    from intecomm_screening.models import SubjectScreening


def raise_if_subject_consent_exists(
    screening_identifier: str | None = None,
    subject_screening: SubjectScreening | None = None,
    is_modelform: bool | None = None,
) -> None:
    """Raises an exception if subject consent model instance exists."""
    screening_identifier = screening_identifier or subject_screening.screening_identifier
    try:
        subject_consent = get_consent_model_cls().objects.get(
            screening_identifier=screening_identifier
        )
    except ObjectDoesNotExist:
        pass
    else:
        if is_modelform:
            if not subject_screening:
                subject_screening = get_subject_screening_model_cls().objects.get(
                    screening_identifier=screening_identifier
                )
            consent_url = get_subject_consent_url(subject_screening=subject_screening)
            msg = format_html(
                'Not allowed. Subject has already consented. See subject <A href="{}">{}</A>',
                mark_safe(consent_url),  # nosec B308 B703
                subject_screening.subject_identifier,
            )
            raise forms.ValidationError(msg)

        else:
            raise AlreadyConsentedError(
                f"Subject has already consented. See {subject_consent.subject_identifier}. "
                f"Perhaps catch this in the form."
            )
