# Generated by Django 4.1.2 on 2022-11-29 05:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_lists", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ReasonsForTesting",
        ),
        migrations.DeleteModel(
            name="RxModificationReasons",
        ),
        migrations.DeleteModel(
            name="RxModifications",
        ),
    ]
