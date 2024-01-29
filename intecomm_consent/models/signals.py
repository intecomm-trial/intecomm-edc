from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from edc_registration.models import RegisteredSubject

from intecomm_screening.models import (
    SubjectScreening,
    SubjectScreeningTz,
    SubjectScreeningUg,
)

from .subject_consent import SubjectConsent
from .subject_consent_tz import SubjectConsentTz
from .subject_consent_ug import SubjectConsentUg


class SubjectConsentDeleteError(Exception):
    pass


def update_subjectconsent(instance, subject_screening_model_cls=None):
    subject_screening = subject_screening_model_cls.objects.get(
        screening_identifier=instance.screening_identifier
    )
    subject_screening.subject_identifier = instance.subject_identifier
    subject_screening.consented = True
    subject_screening.save_base(update_fields=["subject_identifier", "consented"])

    subject_screening.patient_log.subject_identifier = instance.subject_identifier
    subject_screening.patient_log.consent_datetime = instance.consent_datetime
    subject_screening.patient_log.save_base(
        update_fields=["subject_identifier", "consent_datetime"]
    )
    # TODO: is this the right place to do this?
    rs_obj = RegisteredSubject.objects.get(subject_identifier=instance.subject_identifier)
    try:
        rs_obj.full_name = instance.full_name
    except AttributeError:
        pass
    try:
        rs_obj.familiar_name = instance.familiar_name
    except AttributeError:
        pass
    rs_obj.save(update_fields=["full_name", "familiar_name"])


@receiver(
    post_save,
    weak=False,
    sender=SubjectConsent,
    dispatch_uid="update_subjectconsent_on_post_save",
)
def update_subjectconsent_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        if created:
            update_subjectconsent(instance, subject_screening_model_cls=SubjectScreening)


@receiver(
    post_save,
    weak=False,
    sender=SubjectConsentTz,
    dispatch_uid="update_subjectconsenttz_on_post_save",
)
def update_subjectconsenttz_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        if created:
            update_subjectconsent(instance, subject_screening_model_cls=SubjectScreeningTz)


@receiver(
    post_save,
    weak=False,
    sender=SubjectConsentUg,
    dispatch_uid="update_subjectconsentug_on_post_save",
)
def update_subjectconsentug_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        if created:
            update_subjectconsent(instance, subject_screening_model_cls=SubjectScreeningUg)


@receiver(
    pre_delete,
    weak=False,
    sender=SubjectConsent,
    dispatch_uid="subjectconsent_on_pre_delete",
)
def subjectconsent_on_pre_delete(sender, instance, using, **kwargs):
    raise SubjectConsentDeleteError(
        f"Subject consent may not be deleted. Got {instance.subject_identifier}."
    )


@receiver(
    pre_delete,
    weak=False,
    sender=SubjectConsentUg,
    dispatch_uid="subjectconsentug_on_pre_delete",
)
def subjectconsentug_on_pre_delete(sender, instance, using, **kwargs):
    raise SubjectConsentDeleteError(
        f"Subject consent may not be deleted. Got {instance.subject_identifier}."
    )
