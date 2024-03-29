# Generated by Django 4.2.10 on 2024-02-26 13:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_subject", "0147_alter_careseekinga_accompany_num_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bloodresultslft",
            name="alp_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1.0),
                    django.core.validators.MaxValueValidator(9999.99),
                ],
                verbose_name="ALP",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultslft",
            name="alt_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1.0),
                    django.core.validators.MaxValueValidator(9999.99),
                ],
                verbose_name="ALT",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultslft",
            name="alp_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1.0),
                    django.core.validators.MaxValueValidator(9999.99),
                ],
                verbose_name="ALP",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultslft",
            name="alt_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1.0),
                    django.core.validators.MaxValueValidator(9999.99),
                ],
                verbose_name="ALT",
            ),
        ),
    ]
