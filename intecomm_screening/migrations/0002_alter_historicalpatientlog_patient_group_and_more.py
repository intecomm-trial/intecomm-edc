# Generated by Django 4.1.2 on 2022-11-17 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_screening", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalpatientlog",
            name="patient_group",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                help_text="This can be changed at anytime until the group is flagged as COMPLETE. It is recommended to choose a group early in the process.",
                limit_choices_to={"randomized": False, "status__in": ["New", "recruiting"]},
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="intecomm_screening.patientgroup",
                verbose_name="Choose a group (RECOMMENDED)",
            ),
        ),
        migrations.AlterField(
            model_name="patientlog",
            name="patient_group",
            field=models.ForeignKey(
                blank=True,
                help_text="This can be changed at anytime until the group is flagged as COMPLETE. It is recommended to choose a group early in the process.",
                limit_choices_to={"randomized": False, "status__in": ["New", "recruiting"]},
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="intecomm_screening.patientgroup",
                verbose_name="Choose a group (RECOMMENDED)",
            ),
        ),
    ]