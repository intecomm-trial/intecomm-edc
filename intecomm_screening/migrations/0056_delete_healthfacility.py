# Generated by Django 4.2.3 on 2023-07-28 01:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_screening", "0055_delete_identifierformat"),
    ]

    operations = [
        migrations.DeleteModel(
            name="HealthFacility",
        ),
    ]