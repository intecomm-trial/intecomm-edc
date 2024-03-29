# Generated by Django 5.0 on 2023-12-16 15:06

import django.db.models.deletion
import django.db.models.manager
import edc_sites.managers
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "intecomm_screening",
            "0065_patientlogreportprinthistory_intecomm_sc_modifie_891a97_idx_and_more",
        ),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="patientlogreportprinthistory",
            managers=[
                ("on_site", edc_sites.managers.CurrentSiteManager()),
                ("objects", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name="patientlogreportprinthistory",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.site",
            ),
        ),
    ]
