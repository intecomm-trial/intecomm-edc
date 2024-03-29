# Generated by Django 4.1.2 on 2022-11-26 00:58
from django.db import migrations, models
from edc_constants.constants import DM, HIV, HTN


def update_patients_m2ms(apps, schema_editor):
    patient_group_cls = apps.get_model("intecomm_group.patientgroup")
    patient_group_cls.on_site = models.Manager()
    for obj in patient_group_cls._default_manager.all():
        obj.hiv_patients.clear()
        obj.dm_patients.clear()
        obj.htn_patients.clear()
        obj.multi_patients.clear()
        pks = []
        for patient_log in obj.patients.filter(conditions__name__in=[HIV]).exclude(
            conditions__name__in=[DM, HTN]
        ):
            pks.append(patient_log.pk)
            obj.hiv_patients.add(patient_log)
        for patient_log in obj.patients.filter(conditions__name__in=[DM]).exclude(
            conditions__name__in=[HIV, HTN]
        ):
            pks.append(patient_log.pk)
            obj.dm_patients.add(patient_log)
        for patient_log in obj.patients.filter(conditions__name__in=[HTN]).exclude(
            conditions__name__in=[HIV, DM]
        ):
            pks.append(patient_log.pk)
            obj.htn_patients.add(patient_log)
        for patient_log in obj.patients.exclude(pk__in=pks):
            obj.multi_patients.add(patient_log)


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_group", "0008_patientgroup_dm_patients_patientgroup_hiv_patients_and_more"),
    ]

    operations = [migrations.RunPython(update_patients_m2ms)]
