from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from edc_consent.utils import get_consent_model_cls

if TYPE_CHECKING:
    from intecomm_screening.models import SubjectScreening


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
