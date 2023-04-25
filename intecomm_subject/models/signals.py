# create next appt using facility appt date
from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_appointment.constants import (
    COMPLETE_APPT,
    IN_PROGRESS_APPT,
    MISSED_APPT,
    NEW_APPT,
)
from edc_constants.constants import ALIVE, OTHER
from edc_utils import to_utc

from intecomm_lists.models import SubjectVisitMissedReasons

from .next_appointment import NextAppointment
from .subject_visit import SubjectVisit
from .subject_visit_missed import SubjectVisitMissed


def update_appointments(instance):
    appointment = instance.subject_visit.appointment.next
    while appointment:
        if (
            appointment.visit_code == instance.best_visit_code
            and appointment.visit_code_sequence == 0
        ):
            if appointment.appt_status != NEW_APPT:
                break
            appointment.appt_datetime = to_utc(
                datetime(
                    instance.appt_date.year,
                    month=instance.appt_date.month,
                    day=instance.appt_date.day,
                    hour=8,
                    minute=0,
                    tzinfo=ZoneInfo(settings.TIME_ZONE),
                )
            )
            appointment.save()
            break
        else:
            if appointment.appt_status != NEW_APPT:
                appointment = appointment.next
                continue
            appointment.appt_status = IN_PROGRESS_APPT
            appointment.appt_timing = MISSED_APPT
            appointment.save()

            subject_visit = SubjectVisit.objects.get(appointment=appointment)
            subject_visit.report_datetime = appointment.appt_datetime
            subject_visit.save()
            subject_visit_missed = SubjectVisitMissed.objects.create(
                subject_visit=subject_visit,
                survival_status=ALIVE,
                report_datetime=appointment.appt_datetime,
                contact_last_date=None,
            )
            subject_visit_missed.missed_reasons.add(
                SubjectVisitMissedReasons.objects.get(name=OTHER)
            )
            subject_visit_missed.missed_reasons_other = "NOT_SCHEDULED_FOR_FACILITY"
            subject_visit_missed.comment = "[auto-completed by EDC]"
            subject_visit_missed.save()
            appointment.appt_status = COMPLETE_APPT
            appointment.save()
        appointment = appointment.next


@receiver(
    post_save,
    weak=False,
    sender=NextAppointment,
    dispatch_uid="update_next_appointment_on_post_save",
)
def update_next_appointment_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw and not kwargs.get("update_fields"):
        if instance.appt_date and instance.best_visit_code:
            update_appointments(instance)
