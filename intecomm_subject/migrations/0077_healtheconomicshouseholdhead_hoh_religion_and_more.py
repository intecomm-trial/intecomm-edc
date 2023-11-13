# Generated by Django 4.2.3 on 2023-08-03 03:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0076_healtheconomicshouseholdhead_hoh_religion_old_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="healtheconomicshouseholdhead",
            name="hoh_religion",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_he.religions",
                verbose_name="How would you describe the household head’s religious orientation?",
            ),
        ),
        migrations.AddField(
            model_name="healtheconomicspatient",
            name="pat_religion",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_he.religions",
                verbose_name="How would you describe your religious orientation?",
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomicshouseholdhead",
            name="hoh_religion",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_he.religions",
                verbose_name="How would you describe the household head’s religious orientation?",
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomicspatient",
            name="pat_religion",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_he.religions",
                verbose_name="How would you describe your religious orientation?",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicshouseholdhead",
            name="hoh_religion_old",
            field=models.CharField(
                choices=[
                    ("Catholic", "Catholic"),
                    ("Protestant", "Protestant"),
                    ("Muslim", "Muslim"),
                    ("Pentecostal", "Pentecostal"),
                    ("Seventh day Adventist", "Seventh day Adventist"),
                    ("No religion", "No religion"),
                    ("OTHER", "Other, specify ..."),
                ],
                max_length=25,
                verbose_name="How would you describe the household head’s religious orientation?",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicspatient",
            name="pat_religion_old",
            field=models.CharField(
                choices=[
                    ("Catholic", "Catholic"),
                    ("Protestant", "Protestant"),
                    ("Muslim", "Muslim"),
                    ("Pentecostal", "Pentecostal"),
                    ("Seventh day Adventist", "Seventh day Adventist"),
                    ("No religion", "No religion"),
                    ("OTHER", "Other, specify ..."),
                ],
                max_length=25,
                verbose_name="How would you describe your religious orientation?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicshouseholdhead",
            name="hoh_religion_old",
            field=models.CharField(
                choices=[
                    ("Catholic", "Catholic"),
                    ("Protestant", "Protestant"),
                    ("Muslim", "Muslim"),
                    ("Pentecostal", "Pentecostal"),
                    ("Seventh day Adventist", "Seventh day Adventist"),
                    ("No religion", "No religion"),
                    ("OTHER", "Other, specify ..."),
                ],
                max_length=25,
                verbose_name="How would you describe the household head’s religious orientation?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicspatient",
            name="pat_religion_old",
            field=models.CharField(
                choices=[
                    ("Catholic", "Catholic"),
                    ("Protestant", "Protestant"),
                    ("Muslim", "Muslim"),
                    ("Pentecostal", "Pentecostal"),
                    ("Seventh day Adventist", "Seventh day Adventist"),
                    ("No religion", "No religion"),
                    ("OTHER", "Other, specify ..."),
                ],
                max_length=25,
                verbose_name="How would you describe your religious orientation?",
            ),
        ),
    ]
