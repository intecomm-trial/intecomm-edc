from __future__ import annotations

import typing
from decimal import Decimal
from typing import Tuple

from django.urls import reverse
from edc_constants.constants import DM, HIV, HTN
from edc_randomization.site_randomizers import site_randomizers
from edc_randomization.utils import (
    SubjectNotRandomization,
    get_assignment_description_for_subject,
    get_assignment_for_subject,
)
from intecomm_rando.constants import COMM_INTERVENTION

from .exceptions import PatientGroupNotRandomized

if typing.TYPE_CHECKING:
    from .models import PatientGroup


class PatientGroupRatioError(Exception):
    pass


def verify_patient_group_ratio_raise(
    patients, raise_on_outofrange=None
) -> Tuple[int, int, Decimal | None]:
    ncd = 0.0
    hiv = 0.0
    for patient_log in patients:
        if patient_log.conditions.filter(name__in=[DM, HTN]).exclude(name__in=[HIV]).exists():
            ncd += 1.0
        elif (
            patient_log.conditions.filter(name__in=[HIV]).exclude(name__in=[DM, HTN]).exists()
        ):
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


def get_assignment_for_patient_group(group_identifier: str | None) -> str:
    try:
        description = get_assignment_for_subject(
            group_identifier, randomizer_name="default", identifier_fld="group_identifier"
        )
    except SubjectNotRandomization:
        raise PatientGroupNotRandomized("Group is not randomized")
    return description


def get_assignment_description_for_patient_group(group_identifier: str | None) -> str:
    try:
        description = get_assignment_description_for_subject(
            group_identifier, randomizer_name="default", identifier_fld="group_identifier"
        )
    except SubjectNotRandomization:
        raise PatientGroupNotRandomized("Group is not randomized")
    return description


def get_group_subject_dashboards_url(patient_group: PatientGroup | None) -> str | None:
    """Returns a url to the listboard of subjects in followup
    for this group.
    """
    url = None
    randomizer = site_randomizers.get("default")

    if patient_group:
        for obj in randomizer.model_cls().objects.filter(
            group_identifier=patient_group.group_identifier
        ):
            if obj.assignment == COMM_INTERVENTION:
                url = reverse("intecomm_dashboard:comm_subject_listboard_url")
            break
        if not url:
            url = reverse("intecomm_dashboard:inte_subject_listboard_url")
        return f"{url}?q={patient_group.group_identifier}"
    return None
