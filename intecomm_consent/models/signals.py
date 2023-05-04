from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from edc_registration.models import RegisteredSubject

from intecomm_screening.models import SubjectScreening

from .subject_consent import SubjectConsent


class SubjectConsentDeleteError(Exception):
    pass


@receiver(
    post_save,
    weak=False,
    sender=SubjectConsent,
    dispatch_uid="subject_consent_on_post_save",
)
def subject_consent_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        if created:
            subject_screening = SubjectScreening.objects.get(
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
            rs_obj = RegisteredSubject.objects.get(
                subject_identifier=instance.subject_identifier
            )
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
    pre_delete,
    weak=False,
    sender=SubjectConsent,
    dispatch_uid="subject_consent_on_pre_delete",
)
def subject_consent_on_pre_delete(sender, instance, using, **kwargs):
    raise SubjectConsentDeleteError(
        f"Subject consent may not be deleted. Got {instance.subject_identifier}."
    )
