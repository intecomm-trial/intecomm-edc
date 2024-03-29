# Generated by Django 4.2.3 on 2023-07-26 18:14

import edc_facility.model_mixins
import edc_sites.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # ("intecomm_facility", "0002_alter_healthfacility_device_created_and_more"),
        ("intecomm_screening", "0052_auto_20230726_1634"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="IdenfifierFormat",
            new_name="IdentifierFormat",
        ),
        migrations.CreateModel(
            name="HealthFacility",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("intecomm_facility.healthfacility",),
            managers=[
                ("objects", edc_facility.model_mixins.Manager()),
                ("on_site", edc_sites.models.CurrentSiteManager()),
            ],
        ),
    ]
