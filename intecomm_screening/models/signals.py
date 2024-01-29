from __future__ import annotations

from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from edc_utils import get_uuid

from .patient_call import PatientCall
from .patient_log import PatientLog
from .patient_log_ug import PatientLogUg
from .subject_screening import SubjectScreening
from .subject_screening_tz import SubjectScreeningTz
from .subject_screening_ug import SubjectScreeningUg


class SubjectScreeningDeleteError(Exception):
    pass


class PatientLogDeleteError(Exception):
    pass


def update_subjectscreening(instance):
    instance.patient_log.screening_identifier = instance.screening_identifier
    instance.patient_log.screening_datetime = instance.report_datetime
    instance.patient_log.save_base(
        update_fields=["screening_identifier", "screening_datetime"]
    )


def update_subjectscreening_post_delete(instance):
    instance.patient_log.screening_identifier = get_uuid()
    instance.patient_log.screening_datetime = None
    instance.patient_log.save_base(
        update_fields=["screening_identifier", "screening_datetime"]
    )


@receiver(
    post_save,
    weak=False,
    sender=SubjectScreening,
    dispatch_uid="update_subjectscreening_on_post_save",
)
def update_subjectscreening_on_post_save(sender, instance, raw, **kwargs):
    if not raw:
        update_subjectscreening(instance)


@receiver(
    post_save,
    weak=False,
    sender=SubjectScreeningTz,
    dispatch_uid="update_subjectscreeningtz_on_post_save",
)
def update_subjectscreeningtz_on_post_save(sender, instance, raw, **kwargs):
    if not raw:
        update_subjectscreening(instance)


@receiver(
    post_save,
    weak=False,
    sender=SubjectScreeningUg,
    dispatch_uid="update_subjectscreeningug_on_post_save",
)
def update_subjectscreeningug_on_post_save(sender, instance, raw, **kwargs):
    if not raw:
        update_subjectscreening(instance)


@receiver(
    pre_delete,
    weak=False,
    sender=PatientLog,
    dispatch_uid="patientlog_on_pre_delete",
)
def patientlog_on_pre_delete(sender, instance, **kwargs):
    if instance.screening_identifier:
        raise PatientLogDeleteError(
            f"Not allowed. Subject has been screened. Got {instance.screening_identifier}."
        )


@receiver(
    pre_delete,
    weak=False,
    sender=PatientLogUg,
    dispatch_uid="patientlogug_on_pre_delete",
)
def patientlogug_on_pre_delete(sender, instance, **kwargs):
    if instance.screening_identifier:
        raise PatientLogDeleteError(
            f"Not allowed. Subject has been screened. Got {instance.screening_identifier}."
        )


@receiver(
    pre_delete,
    weak=False,
    sender=SubjectScreening,
    dispatch_uid="subjectscreening_on_pre_delete",
)
def subjectscreening_on_pre_delete(sender, instance, **kwargs):
    if instance.consented:
        raise SubjectScreeningDeleteError(
            f"Not allowed. Subject is consented. Got {instance.screening_identifier}."
        )


@receiver(
    pre_delete,
    weak=False,
    sender=SubjectScreeningTz,
    dispatch_uid="subjectscreeningtz_on_pre_delete",
)
def subjectscreeningtz_on_pre_delete(sender, instance, **kwargs):
    if instance.consented:
        raise SubjectScreeningDeleteError(
            f"Not allowed. Subject is consented. Got {instance.screening_identifier}."
        )


@receiver(
    pre_delete,
    weak=False,
    sender=SubjectScreeningUg,
    dispatch_uid="subjectscreeningug_on_pre_delete",
)
def subjectscreeningug_on_pre_delete(sender, instance, **kwargs):
    if instance.consented:
        raise SubjectScreeningDeleteError(
            f"Not allowed. Subject is consented. Got {instance.screening_identifier}."
        )


@receiver(
    post_delete,
    weak=False,
    sender=SubjectScreening,
    dispatch_uid="update_subjectscreening_on_post_delete",
)
def update_subjectscreening_on_post_delete(sender, instance, **kwargs):
    update_subjectscreening_post_delete(instance)


@receiver(
    post_delete,
    weak=False,
    sender=SubjectScreeningTz,
    dispatch_uid="update_subjectscreeningtz_on_post_delete",
)
def update_subjectscreeningtz_on_post_delete(sender, instance, **kwargs):
    update_subjectscreening_post_delete(instance)


@receiver(
    post_delete,
    weak=False,
    sender=SubjectScreeningUg,
    dispatch_uid="update_subjectscreeningug_on_post_delete",
)
def update_subjectscreeningug_on_post_delete(sender, instance, **kwargs):
    update_subjectscreening_post_delete(instance)


@receiver(
    post_save,
    weak=False,
    sender=PatientCall,
    dispatch_uid="update_patient_call_on_post_save",
)
def update_patient_call_on_post_save(sender, instance, raw, created, **kwargs):
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
