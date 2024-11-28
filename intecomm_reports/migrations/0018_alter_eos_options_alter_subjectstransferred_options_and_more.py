# Generated by Django 5.0.8 on 2024-08-27 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_reports", "0017_auto_20240827_0323"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="eos",
            options={
                "default_permissions": ("view", "export", "viewallsites"),
                "managed": False,
                "verbose_name": "End of study",
                "verbose_name_plural": "End of study",
            },
        ),
        migrations.AlterModelOptions(
            name="subjectstransferred",
            options={
                "default_permissions": ("view", "export", "viewallsites"),
                "managed": False,
                "verbose_name": "Subjects Transferred",
                "verbose_name_plural": "Subjects Transferred",
            },
        ),
        migrations.AlterModelOptions(
            name="vl",
            options={
                "default_permissions": ("view", "export", "viewallsites"),
                "managed": False,
                "verbose_name": "Viral loads",
                "verbose_name_plural": "Viral loads",
            },
        ),
    ]