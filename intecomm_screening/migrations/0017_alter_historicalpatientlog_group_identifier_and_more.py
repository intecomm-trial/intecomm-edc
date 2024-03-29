# Generated by Django 4.1.7 on 2023-03-31 02:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_screening", "0016_historicalpatientlog_group_identifier_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalpatientlog",
            name="group_identifier",
            field=models.CharField(
                blank=True,
                help_text="Auto populated when group is randomized",
                max_length=25,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="patientlog",
            name="group_identifier",
            field=models.CharField(
                blank=True,
                help_text="Auto populated when group is randomized",
                max_length=25,
                null=True,
            ),
        ),
    ]
