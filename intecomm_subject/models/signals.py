# create next appt using facility appt date
from django.db.models.signals import post_save
from django.dispatch import receiver

from .next_appointment import NextAppointment


@receiver(
    post_save,
    weak=False,
    sender=NextAppointment,
    dispatch_uid="update_next_appointment_on_post_save",
)
def update_next_appointment_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw and not kwargs.get("update_fields"):
        pass
