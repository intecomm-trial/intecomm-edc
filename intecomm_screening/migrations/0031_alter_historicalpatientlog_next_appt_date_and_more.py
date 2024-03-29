# Generated by Django 4.1.7 on 2023-05-11 16:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_screening", "0030_auto_20230510_0352"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalpatientlog",
            name="next_appt_date",
            field=models.DateField(
                blank=True,
                help_text="If known, this date will help prioritize efforts to contact the patient",
                null=True,
                verbose_name="Next scheduled routine appointment at this health facility",
            ),
        ),
        migrations.AlterField(
            model_name="patientlog",
            name="next_appt_date",
            field=models.DateField(
                blank=True,
                help_text="If known, this date will help prioritize efforts to contact the patient",
                null=True,
                verbose_name="Next scheduled routine appointment at this health facility",
            ),
        ),
    ]
