# Generated by Django 4.2.11 on 2024-07-02 01:06

from django.db import migrations
from edc_qareports.utils import read_unmanaged_model_sql


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_reports", "0005_vl_vlsummary"),
    ]

    operations = [
        migrations.RunSQL(read_unmanaged_model_sql("vl.sql", "intecomm_reports")),
    ]
