from datetime import datetime
from zoneinfo import ZoneInfo

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from edc_randomization.utils import get_object_for_subject
from edc_registration.models import RegisteredSubject
from edc_visit_schedule import site_visit_schedules
from intecomm_rando.constants import CLINIC_CONTROL, COMM_INTERVENTION

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
        elif instance.group_identifier:
            # put subject on schedule once in a group
            rando_obj = get_object_for_subject(
                instance.group_identifier, "default", identifier_fld="group_identifier"
            )
            if rando_obj.assignment in [COMM_INTERVENTION, CLINIC_CONTROL]:
                model_name = (
                    "intecomm_prn.onschedulecomm"
                    if rando_obj.assignment == COMM_INTERVENTION
                    else "intecomm_prn.onscheduleinte"
                )
                _, schedule = site_visit_schedules.get_by_onschedule_model(model_name)
                allocated_datetime = datetime(
                    rando_obj.allocated_datetime.year,
                    rando_obj.allocated_datetime.month,
                    rando_obj.allocated_datetime.day,
                    rando_obj.allocated_datetime.hour,
                    rando_obj.allocated_datetime.minute,
                    rando_obj.allocated_datetime.second,
                    tzinfo=ZoneInfo("UTC"),
                )
                schedule.put_on_schedule(
                    subject_identifier=instance.subject_identifier,
                    onschedule_datetime=allocated_datetime,
                )


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
