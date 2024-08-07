# Generated by Django 5.0.4 on 2024-04-18 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_subject", "0177_alter_careseekingb_accompany_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="careseekinga",
            old_name="travel_time",
            new_name="travel_duration",
        ),
        migrations.RenameField(
            model_name="historicalcareseekinga",
            old_name="travel_time",
            new_name="travel_duration",
        ),
        migrations.AddField(
            model_name="careseekinga",
            name="care_visit_tdelta",
            field=models.DurationField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="careseekinga",
            name="travel_tdelta",
            field=models.DurationField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="careseekinga",
            name="with_hcw_tdelta",
            field=models.DurationField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="careseekingb",
            name="care_visit_tdelta",
            field=models.DurationField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="careseekingb",
            name="travel_tdelta",
            field=models.DurationField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="historicalcareseekinga",
            name="care_visit_tdelta",
            field=models.DurationField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="historicalcareseekinga",
            name="travel_tdelta",
            field=models.DurationField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="historicalcareseekinga",
            name="with_hcw_tdelta",
            field=models.DurationField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="historicalcareseekingb",
            name="care_visit_tdelta",
            field=models.DurationField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="historicalcareseekingb",
            name="travel_tdelta",
            field=models.DurationField(blank=True, editable=False, null=True),
        ),
    ]
