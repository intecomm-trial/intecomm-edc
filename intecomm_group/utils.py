from __future__ import annotations

from decimal import Decimal
from typing import Tuple

from edc_constants.constants import DM, HIV, HTN
from edc_randomization.utils import (
    SubjectNotRandomization,
    get_assignment_description_for_subject,
)

from .exceptions import PatientGroupNotRandomized


class PatientGroupRatioError(Exception):
    pass


def verify_patient_group_ratio_raise(
    patients, raise_on_outofrange=None
) -> Tuple[int, int, Decimal | None]:
    ncd = 0.0
    hiv = 0.0
    for patient_log in patients:
        if patient_log.conditions.filter(name__in=[DM, HTN]).exists():
            ncd += 1.0
        elif patient_log.conditions.filter(name__in=[HIV]).exists():
            hiv += 1.0
    if not ncd or not hiv:
        ratio = 0.0
    else:
        ratio = ncd / hiv
    if raise_on_outofrange and not (2.0 <= ratio <= 2.7):
        raise PatientGroupRatioError(
            f"Ratio NDC:HIV not met. Expected at least 2:1. Got {int(ncd)}:{int(hiv)}. "
            "Perhaps catch this in the form."
        )
    ncd = int(ncd)
    hiv = int(hiv)
    ratio = Decimal(ratio)
    return ncd, hiv, ratio


def get_assignment_description_for_patient_group(group_identifier: str | None) -> str:
    try:
        description = get_assignment_description_for_subject(
            group_identifier, randomizer_name="default"
        )
    except SubjectNotRandomization:
        raise PatientGroupNotRandomized("Group is not randomized")
    return description
