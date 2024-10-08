# Generated by Django 5.0.8 on 2024-08-26 14:55

import django.db.models.deletion
import edc_utils.date
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "intecomm_reports",
            "0011_alter_missingvldrawdates_site_alter_vlsummary_site_and_more",
        ),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vlsummary2",
            name="site",
        ),
        migrations.AlterModelManagers(
            name="diagnoses",
            managers=[],
        ),
        migrations.AlterModelManagers(
            name="missingvldrawdates",
            managers=[],
        ),
        migrations.AddField(
            model_name="diagnoses",
            name="report_model",
            field=models.CharField(default="meta_reports.diagnoses", max_length=50),
        ),
        migrations.AlterField(
            model_name="diagnoses",
            name="created",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="diagnoses",
            name="site",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="sites.site"
            ),
        ),
        migrations.CreateModel(
            name="VlSummary6m",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("subject_identifier", models.CharField(max_length=50, unique=True)),
                ("created", models.DateTimeField(default=edc_utils.date.get_utcnow)),
                ("baseline_date", models.DateField(null=True)),
                ("baseline_vl_date", models.DateField(null=True)),
                ("endline_vl_date", models.DateField(null=True)),
                ("baseline_vl", models.IntegerField(null=True)),
                ("endline_vl", models.IntegerField(null=True)),
                ("offschedule_date", models.DateField(null=True)),
                ("last_vl_date", models.DateField(null=True)),
                ("next_vl_date", models.DateField(null=True)),
                ("expected", models.BooleanField(null=True)),
                ("offset", models.IntegerField(null=True)),
                (
                    "report_model",
                    models.CharField(default="intecomm_reports.vlsummary9m", max_length=50),
                ),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="sites.site"
                    ),
                ),
            ],
            options={
                "verbose_name": "Viral load summary (endline >= 6m)",
                "verbose_name_plural": "Viral load summary (endline >= 6m)",
            },
        ),
        migrations.CreateModel(
            name="VlSummary9m",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("subject_identifier", models.CharField(max_length=50, unique=True)),
                ("created", models.DateTimeField(default=edc_utils.date.get_utcnow)),
                ("baseline_date", models.DateField(null=True)),
                ("baseline_vl_date", models.DateField(null=True)),
                ("endline_vl_date", models.DateField(null=True)),
                ("baseline_vl", models.IntegerField(null=True)),
                ("endline_vl", models.IntegerField(null=True)),
                ("offschedule_date", models.DateField(null=True)),
                ("last_vl_date", models.DateField(null=True)),
                ("next_vl_date", models.DateField(null=True)),
                ("expected", models.BooleanField(null=True)),
                ("offset", models.IntegerField(null=True)),
                (
                    "report_model",
                    models.CharField(default="intecomm_reports.vlsummary6m", max_length=50),
                ),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="sites.site"
                    ),
                ),
            ],
            options={
                "verbose_name": "Viral load summary (endline >= 9m)",
                "verbose_name_plural": "Viral load summary (endline >= 9m)",
            },
        ),
        migrations.DeleteModel(
            name="VlSummary",
        ),
        migrations.DeleteModel(
            name="VlSummary2",
        ),
    ]
