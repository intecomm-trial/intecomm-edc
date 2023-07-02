# Generated by Django 4.2.1 on 2023-07-02 12:48

from django.db import migrations
from django.db.migrations import RunPython
from tqdm import tqdm


def update_patient_log_identifier(apps, schema_editor):
    subjectscreening_cls = apps.get_model("intecomm_screening.subjectscreening")
    qs = subjectscreening_cls.objects.all()
    for subjectscreening in tqdm(qs, total=qs.count()):
        subjectscreening.patient_log_identifier = (
            subjectscreening.patient_log.patient_log_identifier
        )
        subjectscreening.save_base(update_fields=["patient_log_identifier"])


class Migration(migrations.Migration):
    dependencies = [
        (
            "intecomm_screening",
            "0040_historicalsubjectscreening_patient_log_identifier_and_more",
        ),
    ]

    operations = [RunPython(update_patient_log_identifier)]
