# Generated by Django 4.2.11 on 2024-04-22 16:49
from django.db import migrations
from django.db.migrations import RunPython
from tqdm import tqdm

from intecomm_lists.models import HtnManagement


def update_m2m_from_charfield(apps, schema_editor):
    model_cls = apps.get_model("intecomm_subject", "htnreview")
    qs = model_cls.objects.all()
    total = qs.count()
    for obj in tqdm(qs, total=total):
        htn_management = HtnManagement.objects.get(name=obj.managed_by_old)
        obj.managed_by.add(htn_management.id)
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_subject", "0180_historicalhtnreview_managed_by_other_and_more"),
    ]

    operations = [RunPython(update_m2m_from_charfield)]