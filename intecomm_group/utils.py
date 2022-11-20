from decimal import Decimal
from typing import Tuple

from edc_constants.constants import DM, HIV, HTN


class PatientGroupRatioError(Exception):
    pass


def verify_patient_group_ratio_raise(
    patients, raise_on_outofrange=None
) -> Tuple[int, int, Decimal]:
    ncd = 0.0
    hiv = 0.0
    for patient_log in patients:
        if patient_log.conditions.filter(name__in=[DM, HTN]).exists():
            ncd += 1.0
        if patient_log.conditions.filter(name__in=[HIV]).exists():
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
