from __future__ import annotations

from decimal import Decimal
from typing import Tuple

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from edc_constants.constants import DM, HIV, HTN
from edc_randomization.site_randomizers import site_randomizers
from edc_randomization.utils import (
    SubjectNotRandomization,
    get_assignment_description_for_subject,
    get_assignment_for_subject,
)
from intecomm_rando.constants import COMMUNITY_ARM

from .exceptions import PatientGroupNotRandomized
from .models import PatientGroup
from .patient_group_updater import PatientGroupUpdater, PatientGroupUpdaterError


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
    """Returns an url to the listboard of subjects in followup
    for this group.
    """
    url = None
    randomizer = site_randomizers.get("default")

    if patient_group:
        for obj in randomizer.model_cls().objects.filter(
            group_identifier=patient_group.group_identifier
        ):
            if obj.assignment == COMMUNITY_ARM:
                url = reverse("intecomm_dashboard:subject_listboard_url")
            break
        if not url:
            url = reverse("intecomm_dashboard:subject_listboard_url")
        return f"{url}?q={patient_group.group_identifier}"
    return None


def add_subjects_to_group(group_name: str, subject_identifiers: list[str]):
    """Add subjects to a group after the group has randomized.

    Use with caution.

    The update will work for a participant if:
        * The patient group exists and has been randomized
        * The participant to be added is NOT already in a patient
          group.
        * The participant to be added has been entered into the
          PatientLog, screened and consented.
    """
    try:
        patient_group = PatientGroup.objects.get(name=group_name)
    except ObjectDoesNotExist:
        print(f"PatientGroup does not exist. Got {group_name}.")
    else:
        status = patient_group.status
        for subject_identifier in subject_identifiers:
            try:
                updater = PatientGroupUpdater(patient_group, subject_identifier)
            except PatientGroupUpdaterError as e:
                print(f"    - skipping: {e}")
            except PatientGroupNotRandomized as e:
                print(f"{e}")
                break
            else:
                try:
                    updater.add_subject_to_group()
                except PatientGroupUpdaterError as e:
                    print(f"   - failed: {e}")
                else:
                    print(f"    - added {subject_identifier}")
        patient_group.status = status
        patient_group.save()
