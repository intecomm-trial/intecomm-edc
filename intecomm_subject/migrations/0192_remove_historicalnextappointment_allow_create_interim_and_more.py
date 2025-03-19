# Generated by Django 6.0 on 2025-02-05 01:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_subject", "0191_alter_historicalnextappointment_appt_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalnextappointment",
            name="allow_create_interim",
        ),
        migrations.RemoveField(
            model_name="nextappointment",
            name="allow_create_interim",
        ),
        migrations.AlterField(
            model_name="historicalnextappointment",
            name="appt_date",
            field=models.DateField(
                default=django.utils.timezone.now,
                help_text="Should fall on an valid clinic day for this facility",
                verbose_name="Next scheduled routine/facility appointment",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="historicalnextappointment",
            name="appt_datetime",
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name="nextappointment",
            name="appt_date",
            field=models.DateField(
                default=django.utils.timezone.now,
                help_text="Should fall on an valid clinic day for this facility",
                verbose_name="Next scheduled routine/facility appointment",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="nextappointment",
            name="appt_datetime",
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]
