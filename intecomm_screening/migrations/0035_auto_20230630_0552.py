# Generated by Django 4.2.1 on 2023-06-30 02:52
from uuid import uuid4

from django.db import migrations
from django.db.migrations import RunPython
from edc_utils import get_uuid
from tqdm import tqdm


def update_identifiers_from_null_to_uuid(apps, schema_editor):
    model_cls = apps.get_model("intecomm_screening.patientlog")
    qs = model_cls.objects.filter(screening_identifier__isnull=True)
    for obj in tqdm(qs, total=qs.count()):
        obj.screening_identifier = get_uuid()
        obj.save_base(update_fields=["screening_identifier"])
    qs = model_cls.objects.filter(subject_identifier__isnull=True)
    for obj in tqdm(qs, total=qs.count()):
        obj.subject_identifier = get_uuid()
        obj.save_base(update_fields=["subject_identifier"])


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_screening", "0034_alter_consentrefusal_screening_identifier_and_more"),
    ]

    operations = [RunPython(update_identifiers_from_null_to_uuid)]
