# Generated by Django 5.0.4 on 2024-04-15 20:48

from django.db import migrations

import intecomm_subject.models.fields.duration_field


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_subject", "0170_remove_careseekinga_accompany_lost_income_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="careseekinga",
            name="travel_time",
            field=intecomm_subject.models.fields.duration_field.DurationAsStringField(
                metadata="FTRATIME1",
                null=True,
                verbose_name="How long did it take you to reach here?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="travel_time",
            field=intecomm_subject.models.fields.duration_field.DurationAsStringField(
                metadata="FTRATIME1",
                null=True,
                verbose_name="How long did it take you to reach here?",
            ),
        ),
    ]
