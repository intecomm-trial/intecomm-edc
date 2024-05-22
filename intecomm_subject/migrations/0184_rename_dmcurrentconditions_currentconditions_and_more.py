# Generated by Django 4.2.11 on 2024-05-22 21:30

from django.db import migrations, models
import django.db.models.manager
import edc_sites.managers


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("intecomm_subject", "0183_alter_dmcurrentconditions_dm_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="DmCurrentConditions",
            new_name="CurrentConditions",
        ),
        migrations.AlterModelManagers(
            name="currentconditions",
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", edc_sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.RenameIndex(
            model_name="currentconditions",
            new_name="intecomm_su_modifie_490726_idx",
            old_name="intecomm_su_modifie_12b4ab_idx",
        ),
        migrations.RenameIndex(
            model_name="currentconditions",
            new_name="intecomm_su_user_mo_15c1bf_idx",
            old_name="intecomm_su_user_mo_596162_idx",
        ),
        migrations.RemoveField(
            model_name="bloodresultsins",
            name="fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="dminitialreview",
            name="glucose_fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="dmreview",
            name="glucose_fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="glucose",
            name="glucose_fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="historicalbloodresultsins",
            name="fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="historicaldminitialreview",
            name="glucose_fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="historicaldmreview",
            name="glucose_fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="historicalglucose",
            name="glucose_fasting_duration_minutes",
        ),
        migrations.AddField(
            model_name="bloodresultsins",
            name="fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="dminitialreview",
            name="glucose_fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="dmreview",
            name="glucose_fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="glucose",
            name="glucose_fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsins",
            name="fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="historicaldminitialreview",
            name="glucose_fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="historicaldmreview",
            name="glucose_fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="historicalglucose",
            name="glucose_fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
    ]