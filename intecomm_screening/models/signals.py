from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_constants.constants import YES

from ..randomize_group import randomize_group
from .patient_group import PatientGroup
from .patient_log import PatientLog
from .utils import add_to_group, remove_from_group


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
    dispatch_uid="randomize_group_on_post_save",
)
def randomize_group_on_post_save(sender, instance, raw, **kwargs):
    if not raw:
        if not instance.randomized and instance.randomize == YES:
            instance.randomized, instance.modified, instance.user_modified = randomize_group(
                instance
            )
            instance.save_base(update_fields=["randomized", "modified", "user_modified"])
