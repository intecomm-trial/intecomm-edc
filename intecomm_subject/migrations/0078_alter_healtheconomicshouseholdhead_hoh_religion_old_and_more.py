# Generated by Django 4.2.3 on 2023-08-03 03:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0077_healtheconomicshouseholdhead_hoh_religion_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="healtheconomicshouseholdhead",
            name="hoh_religion_old",
            field=models.CharField(
                max_length=25,
                verbose_name="How would you describe the household head’s religious orientation?",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicspatient",
            name="pat_religion_old",
            field=models.CharField(
                max_length=25,
                verbose_name="How would you describe your religious orientation?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicshouseholdhead",
            name="hoh_religion_old",
            field=models.CharField(
                max_length=25,
                verbose_name="How would you describe the household head’s religious orientation?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicspatient",
            name="pat_religion_old",
            field=models.CharField(
                max_length=25,
                verbose_name="How would you describe your religious orientation?",
            ),
        ),
    ]
