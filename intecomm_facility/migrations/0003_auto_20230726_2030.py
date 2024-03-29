# Generated by Django 4.2.3 on 2023-07-26 17:30
from django.db import migrations
from edc_list_data import PreloadData
from tqdm import tqdm

from intecomm_facility.list_data import list_data


def update_healthfacility(apps, schema_editor):
    healthfacility_old_model_cls = apps.get_model("intecomm_screening", "oldhealthfacility")
    healthfacility_model_cls = apps.get_model("intecomm_facility", "healthfacility")
    healthfacilitytype_old_model_cls = apps.get_model("intecomm_lists", "healthfacilitytypes")
    healthfacilitytype_model_cls = apps.get_model("edc_facility", "healthfacilitytypes")

    PreloadData(list_data=list_data, apps=apps)

    # populate new health facility model
    total = healthfacility_old_model_cls.objects.all().count()
    print("\n")
    for obj_old in tqdm(healthfacility_old_model_cls.objects.all(), total=total):
        obj_new = healthfacility_model_cls()
        for fld in healthfacility_model_cls._meta.get_fields():
            if fld.name in ["nextappointment", "healthtalklog"]:
                continue
            fldname = fld.name
            if fld.name == "sun":
                setattr(obj_new, fldname, False)
            else:
                try:
                    value = getattr(obj_old, f"{fld.name}_id")
                except AttributeError:
                    value = getattr(obj_old, fld.name)
                else:
                    if fld.name == "health_facility_type":
                        old_name = healthfacilitytype_old_model_cls.objects.get(
                            id=getattr(obj_old, f"{fld.name}_id")
                        ).name
                        value = healthfacilitytype_model_cls.objects.get(name=old_name).id
                    fldname = f"{fld.name}_id"
                setattr(obj_new, fldname, value)
        obj_new.save()


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_facility", "0002_alter_healthfacility_device_created_and_more"),
        ("intecomm_screening", "0045_alter_consentrefusal_options_and_more"),
    ]

    operations = [migrations.RunPython(update_healthfacility)]
