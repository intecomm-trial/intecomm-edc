from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_constants.constants import YES
from intecomm_form_validators.screening.patient_group_form_validator import (
    calculate_ratio,
)

from ..randomize_group import randomize_group
from .patient_group import PatientGroup
from .patient_log import PatientLog
from .subject_screening import SubjectScreening
from .utils import add_to_group, remove_from_group


class PatientGroupRatioError(Exception):
    pass


@receiver(
    post_save,
    weak=False,
    sender=PatientLog,
    dispatch_uid="update_patient_group_membership_on_post_save",
)
def update_patient_group_membership_on_post_save(sender, instance, raw, **kwargs):
    if not raw:
        remove_from_group(instance)
        if instance.patient_group:
            add_to_group(instance)


@receiver(
    post_save,
    weak=False,
    sender=PatientGroup,
    dispatch_uid="update_patient_group_ratio_on_post_save",
)
def update_patient_group_ratio_on_post_save(sender, instance, raw, update_fields, **kwargs):
    if not raw and not update_fields:
        ncd, hiv = calculate_ratio(instance.patients.all())
        instance.ratio = ncd / hiv
        if not (2.0 <= instance.ratio <= 2.7):
            raise PatientGroupRatioError(
                f"Ratio NDC:HIV not met. Expected at least 2:1. Got {int(ncd)}:{int(hiv)}. "
                "Perhaps catch this in the form."
            )
        instance.save_base(update_fields=["ratio"])


@receiver(
    post_save,
    weak=False,
    sender=PatientGroup,
    dispatch_uid="randomize_group_on_post_save",
)
def randomize_group_on_post_save(sender, instance, raw, **kwargs):
    if not raw:
        if not instance.randomized and instance.randomize == YES:
            instance.randomized, instance.modified, instance.user_modified = randomize_group(
                instance
            )
            instance.save_base(update_fields=["randomized", "modified", "user_modified"])


@receiver(
    post_save,
    weak=False,
    sender=SubjectScreening,
    dispatch_uid="update_subjectscreening_on_post_save",
)
def update_subjectscreening_on_post_save(sender, instance, raw, **kwargs):
    if not raw:
        instance.patient_log.screening_identifier = instance.screening_identifier
        instance.patient_log.screening_datetime = instance.report_datetime
        instance.patient_log.save_base(
            update_fields=["screening_identifier", "screening_datetime"]
        )
