# Generated by Django 4.1.7 on 2023-05-01 19:08
from django.db import migrations
from django.db.migrations import RunPython
from tqdm import tqdm

from intecomm_screening.models.patient_log import FilingIdentifier


def update_filing_identifier(apps, schema_editor):
    patientlog_cls = apps.get_model("intecomm_screening", "patientlog")
    total = patientlog_cls.objects.filter(filing_identifier__isnull=True).count()
    for obj in tqdm(
        patientlog_cls.objects.all().order_by("site_id", "created"),
        total=total,
    ):
        obj.filing_identifier = FilingIdentifier(site_id=obj.site_id).identifier
        obj.save_base(update_fields=["filing_identifier"])


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_screening", "0022_historicalpatientlog_filing_identifier_and_more"),
    ]

    operations = [RunPython(update_filing_identifier)]
