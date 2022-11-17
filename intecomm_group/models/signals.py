from __future__ import annotations

import re

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from edc_constants.constants import COMPLETE, UUID_PATTERN, YES
from edc_randomization.randomizer import RandomizationError

from ..randomize_group import randomize_group
from ..utils import calculate_ratio
from .patient_group import PatientGroup
from .patient_group_appointment import PatientGroupAppointment
from .patient_group_meeting import PatientGroupMeeting
from .proxy_models import PatientLog
from .utils import add_to_group, remove_from_group


@receiver(
    post_save,
    weak=False,
    sender=PatientLog,
    dispatch_uid="update_patient_group_membership_on_patient_log_post_save",
)
def update_patient_group_on_patient_log_post_save(
    sender, instance, raw, update_fields, **kwargs
):
    if not raw and not update_fields:
        remove_from_group(instance)
        if instance.patient_group:
            add_to_group(instance)


@receiver(
    m2m_changed,
    weak=False,
    # sender=PatientGroup,
    dispatch_uid="update_patient_log_on_patient_group_m2m_change",
)
def update_patient_log_on_patient_group_m2m_change(action, instance, pk_set, **kwargs):
    if isinstance(instance, PatientGroup):
        if action == "post_remove":
            for pk in pk_set:
                patient_log = PatientLog.objects.get(id=pk)
                patient_log.patient_group = None
                patient_log.save_base(update_fields=["patient_group"])
        elif action == "post_add":
            for pk in pk_set:
                patient_log = PatientLog.objects.get(id=pk)
                patient_log.patient_group = instance
                patient_log.save_base(update_fields=["patient_group"])


@receiver(
    post_save,
    weak=False,
    sender=PatientGroup,
    dispatch_uid="update_patient_group_ratio_on_post_save",
)
def update_patient_group_ratio_on_post_save(sender, instance, raw, update_fields, **kwargs):
    if not raw and not update_fields:
        raise_on_outofrange = True if instance.status == COMPLETE else False
        ncd, hiv, ratio = calculate_ratio(
            instance.patients.all(), raise_on_outofrange=raise_on_outofrange
        )
        instance.ratio = ratio
        instance.save_base(update_fields=["ratio"])


@receiver(
    post_save,
    weak=False,
    sender=PatientGroup,
    dispatch_uid="randomize_group_on_post_save",
)
def randomize_patient_group_on_post_save(sender, instance, raw, **kwargs):
    if not raw:
        if not instance.randomized and instance.randomize_now == YES:
            if not re.match(UUID_PATTERN, instance.group_identifier):
                raise RandomizationError(
                    "Failed to randomize group. Group identifier is not a uuid. "
                    f"Has this group already been randomized? Got {instance.group_identifier}."
                )
            # randomize group
            (
                instance.randomized,
                instance.modified,
                instance.user_modified,
                instance.group_identifier,
            ) = randomize_group(instance)
            # save to patient group
            instance.save_base(
                update_fields=[
                    "randomized",
                    "group_identifier",
                    "modified",
                    "user_modified",
                ]
            )


@receiver(
    post_save,
    dispatch_uid="create_or_update_refills_on_post_save",
    sender=PatientGroupAppointment,
)
def create_or_update_patient_group_meeting_on_post_save(
    sender, instance, raw, created, update_fields, **kwargs
):
    if not raw:
        try:
            PatientGroupMeeting.objects.get(patient_group_appointment=instance)
        except ObjectDoesNotExist:
            PatientGroupMeeting.objects.create(
                patient_group_appointment=instance,
            )
