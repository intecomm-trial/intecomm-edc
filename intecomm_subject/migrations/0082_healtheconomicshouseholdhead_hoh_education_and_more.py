# Generated by Django 4.2.3 on 2023-08-03 15:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("edc_he", "0006_historicalhealtheconomicsproperty_and_more"),
        ("intecomm_subject", "0081_healtheconomicshouseholdhead_hoh_education_old_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="healtheconomicshouseholdhead",
            name="hoh_education",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_he.education",
                verbose_name="Highest level of education completed by the household head?",
            ),
        ),
        migrations.AddField(
            model_name="healtheconomicshouseholdhead",
            name="hoh_employment_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_he.employment",
                verbose_name="Household head’s type of employment",
            ),
        ),
        migrations.AddField(
            model_name="healtheconomicspatient",
            name="pat_education",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_he.education",
                verbose_name="Highest level of education completed?",
            ),
        ),
        migrations.AddField(
            model_name="healtheconomicspatient",
            name="pat_employment_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_he.employment",
                verbose_name="What is your type of employment?",
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomicshouseholdhead",
            name="hoh_education",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_he.education",
                verbose_name="Highest level of education completed by the household head?",
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomicshouseholdhead",
            name="hoh_employment_type",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_he.employment",
                verbose_name="Household head’s type of employment",
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomicspatient",
            name="pat_education",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_he.education",
                verbose_name="Highest level of education completed?",
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomicspatient",
            name="pat_employment_type",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_he.employment",
                verbose_name="What is your type of employment?",
            ),
        ),
    ]
