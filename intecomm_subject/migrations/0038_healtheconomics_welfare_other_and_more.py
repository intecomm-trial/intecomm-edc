# Generated by Django 4.1.7 on 2023-04-25 02:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0037_alter_bloodresultsins_fasting_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="healtheconomics",
            name="welfare_other",
            field=models.TextField(
                blank=True, max_length=250, null=True, verbose_name="If yes, please explain"
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomics",
            name="welfare_other",
            field=models.TextField(
                blank=True, max_length=250, null=True, verbose_name="If yes, please explain"
            ),
        ),
    ]
