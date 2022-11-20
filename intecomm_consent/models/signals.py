from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from intecomm_screening.models import SubjectScreening
from intecomm_subject.models import SubjectVisit

from .subject_consent import SubjectConsent


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
            # put subject on schedule
            _, schedule = site_visit_schedules.get_by_onschedule_model(
                "intecomm_prn.onschedulebaseline"
            )
            schedule.put_on_schedule(
                subject_identifier=instance.subject_identifier,
                onschedule_datetime=instance.consent_datetime,
            )


@receiver(
    post_delete,
    weak=False,
    sender=SubjectConsent,
    dispatch_uid="subject_consent_on_post_delete",
)
def subject_consent_on_post_delete(sender, instance, using, **kwargs):
    """Updates/Resets subject screening."""
    # don't allow if subject visits exist. This should be caught
    # in the ModelAdmin delete view
    if SubjectVisit.objects.filter(subject_identifier=instance.subject_identifier).exists():
        raise ValidationError("Unable to delete consent. Visit data exists.")

    _, schedule = site_visit_schedules.get_by_onschedule_model(
        "intecomm_prn.onschedulebaseline"
    )
    schedule.take_off_schedule(
        subject_identifier=instance.subject_identifier,
        offschedule_datetime=instance.consent_datetime,
    )

    # update subject screening
    subject_screening = SubjectScreening.objects.get(
        screening_identifier=instance.screening_identifier
    )
    subject_screening.consented = False
    subject_screening.subject_identifier = subject_screening.subject_screening_as_pk
    subject_screening.save()
