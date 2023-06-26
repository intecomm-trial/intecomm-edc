from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from edc_consent.utils import get_consent_model_cls


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
            f"Multiple consents detected for {screening_identifier}. "
            f"Perhaps catch this in the form."
        )
    else:
        raise AlreadyConsentedError(
            f"Subject has already consented. See {subject_consent.subject_identifier}. "
            f"Perhaps catch this in the form."
        )
