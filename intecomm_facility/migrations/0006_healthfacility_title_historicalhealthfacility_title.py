# Generated by Django 6.0 on 2025-01-30 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_facility", "0005_alter_healthfacility_site_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="healthfacility",
            name="title",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="historicalhealthfacility",
            name="title",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
