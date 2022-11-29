from __future__ import annotations

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .patient_call import PatientCall
from .proxy_models import PatientGroup
from .subject_screening import SubjectScreening


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


@receiver(
    post_save,
    weak=False,
    sender=PatientCall,
    dispatch_uid="patient_call_on_post_save",
)
def patient_call_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        qs = sender.objects.filter(patient_log=instance.patient_log)
        instance.patient_log.call_attempts = qs.count()
        instance.patient_log.save(update_fields=["call_attempts"])


@receiver(
    post_delete,
    weak=False,
    sender=PatientCall,
    dispatch_uid="patient_call_on_post_delete",
)
def patient_call_on_post_delete(sender, instance, using, **kwargs):
    instance.patient_log.call_attempts = (
        0
        if instance.patient_log.call_attempts == 0
        else instance.patient_log.call_attempts - 1
    )
    instance.patient_log.save(update_fields=["call_attempts"])


@receiver(
    post_save,
    weak=False,
    sender=PatientGroup,
    dispatch_uid="patient_group_on_post_save",
)
def patient_group_on_post_save(sender, instance, raw, created, **kwargs):
    pass
    # instance.patients.clear()
