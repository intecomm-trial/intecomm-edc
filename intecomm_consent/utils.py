from django.core.exceptions import ObjectDoesNotExist
from edc_consent.utils import get_consent_model_cls


class AlreadyConsentedError(Exception):
    pass


def raise_if_already_consented(screening_identifier: str):
    try:
        subject_consent = get_consent_model_cls().objects.get(
            screening_identifier=screening_identifier
        )
    except ObjectDoesNotExist:
        subject_consent = None

    if subject_consent:
        raise AlreadyConsentedError(
            "Subject has already consented. "
            f"See {subject_consent.subject_identifier}. "
            f"Perhaps catch this in the form."
        )
