from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import PatientGroupMeeting
from .patient_group_appointment import PatientGroupAppointment


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
