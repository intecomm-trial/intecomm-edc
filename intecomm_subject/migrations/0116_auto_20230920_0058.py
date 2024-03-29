# Generated by Django 4.2.5 on 2023-09-19 21:58
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations
from django.db.migrations import RunPython
from django.db.models import ProtectedError
from edc_appointment.constants import MISSED_APPT, SKIPPED_APPT
from edc_appointment.utils import reset_appointment
from edc_metadata.models import CrfMetadata
from tqdm import tqdm


def delete_subject_visit_missed(apps, schema_editor):
    model_cls = apps.get_model("intecomm_subject.subjectvisitmissed")
    appointment_model_cls = apps.get_model("edc_appointment.appointment")
    subject_visit_model_cls = apps.get_model("intecomm_subject.subjectvisit")

    qs = model_cls.objects.filter(missed_reasons_other="NOT_SCHEDULED_FOR_FACILITY")
    total = qs.count()
    for subject_visit_missed in tqdm(qs, total=total):
        subject_visit_id = subject_visit_missed.subject_visit_id
        subject_visit = subject_visit_model_cls.objects.get(id=subject_visit_id)
        crf_metadata = CrfMetadata.objects.filter(
            model=subject_visit_missed._meta.label_lower,
            visit_schedule_name=subject_visit.visit_schedule_name,
            schedule_name=subject_visit.schedule_name,
            visit_code=subject_visit.visit_code,
            visit_code_sequence=0,
            subject_identifier=subject_visit.subject_identifier,
        )
        subject_visit_missed.delete()
        crf_metadata.delete()
        try:
            subject_visit = subject_visit_model_cls.objects.get(id=subject_visit_id)
        except ObjectDoesNotExist:
            pass
        else:
            appointment_id = subject_visit.appointment_id
            subject_visit.delete()
            appointment = appointment_model_cls.objects.get(id=appointment_id)
            appointment.related_visit = None
            reset_appointment(appointment)

    appointments = appointment_model_cls.objects.filter(
        appt_type_id__isnull=True,
        appt_timing__in=[MISSED_APPT, SKIPPED_APPT],
        visit_code_sequence=0,
    ).order_by("subject_identifier")
    total = appointments.count()
    for appointment in tqdm(appointments, total=total):
        try:
            obj = subject_visit_model_cls.objects.get(appointment_id=appointment.id)
        except ObjectDoesNotExist:
            appointment.related_visit = None
            reset_appointment(appointment)
        else:
            try:
                obj.delete()
            except ProtectedError as e:
                print(e)
            else:
                appointment.related_visit = None
                reset_appointment(appointment)


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0115_remove_historicalnextappointment_best_visit_code_and_more"),
    ]

    operations = [RunPython(delete_subject_visit_missed)]
