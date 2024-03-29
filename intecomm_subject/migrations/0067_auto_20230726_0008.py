# Generated by Django 4.2.3 on 2023-07-25 21:10
from django.db import migrations
from tqdm import tqdm


def update_next_appointment(apps, schema_editor):
    """Update healthfacility FK from old healthfacility model to
    new healthfacility model.
    """
    model_cls = apps.get_model("intecomm_subject", "nextappointment")
    healthfacility_model_cls = apps.get_model("intecomm_facility", "healthfacility")
    healthfacility_old_model_cls = apps.get_model("intecomm_screening", "healthfacility")
    total = model_cls.objects.all().count()
    print("\n")
    for obj in tqdm(model_cls.objects.all(), total=total):
        if not obj.old_health_facility:
            continue
        old_health_facility = healthfacility_old_model_cls.objects.get(
            id=obj.old_health_facility
        )
        obj.health_facility_id = healthfacility_model_cls.objects.get(
            name=old_health_facility.name
        ).id
        obj.save_base(update_fields=["health_facility_id"])
    print("\n")


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0066_historicalnextappointment_health_facility_and_more"),
    ]

    operations = [migrations.RunPython(update_next_appointment)]
