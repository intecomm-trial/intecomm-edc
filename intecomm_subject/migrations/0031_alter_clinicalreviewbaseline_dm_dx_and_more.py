# Generated by Django 4.1.7 on 2023-04-19 03:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0030_nextappointment_historicalnextappointment_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clinicalreviewbaseline",
            name="dm_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Has the patient ever been diagnosed with Diabetes?",
            ),
        ),
        migrations.AlterField(
            model_name="clinicalreviewbaseline",
            name="hiv_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Has the patient ever tested <U>positive</U> for HIV infection?",
            ),
        ),
        migrations.AlterField(
            model_name="clinicalreviewbaseline",
            name="htn_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Has the patient ever been diagnosed with Hypertension?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalclinicalreviewbaseline",
            name="dm_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Has the patient ever been diagnosed with Diabetes?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalclinicalreviewbaseline",
            name="hiv_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Has the patient ever tested <U>positive</U> for HIV infection?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalclinicalreviewbaseline",
            name="htn_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Has the patient ever been diagnosed with Hypertension?",
            ),
        ),
    ]
