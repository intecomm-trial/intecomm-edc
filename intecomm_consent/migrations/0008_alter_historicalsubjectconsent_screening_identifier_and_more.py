# Generated by Django 4.2.1 on 2023-06-30 02:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_consent", "0007_alter_historicalsubjectconsent_language_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="screening_identifier",
            field=models.CharField(
                db_index=True,
                max_length=50,
                validators=[django.core.validators.RegexValidator("^[A-Z0-9]+$")],
                verbose_name="Screening identifier",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="screening_identifier",
            field=models.CharField(
                max_length=50,
                unique=True,
                validators=[django.core.validators.RegexValidator("^[A-Z0-9]+$")],
                verbose_name="Screening identifier",
            ),
        ),
    ]
