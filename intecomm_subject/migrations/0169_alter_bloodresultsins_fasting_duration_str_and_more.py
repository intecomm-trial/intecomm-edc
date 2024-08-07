# Generated by Django 5.0.4 on 2024-04-15 12:34

import django.core.validators
import edc_model_fields.fields.custom_django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_subject", "0168_alter_careseekinga_money_source_main_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bloodresultsins",
            name="fasting_duration_str",
            field=models.CharField(
                blank=True,
                help_text="As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc",
                max_length=8,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long have they fasted in hours and/or minutes?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekinga",
            name="care_visit_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FFACTIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How much time did you spend during your visit today -- from arrival to this place until the end of your visit?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekinga",
            name="travel_time",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FTRATIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long did it take you to reach here?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekinga",
            name="wait_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FWAITIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How much time did you spend waiting?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekinga",
            name="with_hcw_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FWORKTIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How much time did you spend with the healthcare worker?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekingb",
            name="care_visit_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="in hours and minutes (format HH:MM)",
                max_length=5,
                metadata="FOUTTIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="Roughly how much time did you spend during your last/most recent visit?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekingb",
            name="travel_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="in hours and minutes (format HH:MM)",
                max_length=5,
                metadata="FOUTTRATIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long did it take you to get there?",
            ),
        ),
        migrations.AlterField(
            model_name="dminitialreview",
            name="glucose_fasting_duration_str",
            field=models.CharField(
                blank=True,
                help_text="As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc",
                max_length=8,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long did they fast (in hours and minutes)?",
            ),
        ),
        migrations.AlterField(
            model_name="dmreview",
            name="glucose_fasting_duration_str",
            field=models.CharField(
                blank=True,
                help_text="As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc",
                max_length=8,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long have they fasted in hours and/or minutes?",
            ),
        ),
        migrations.AlterField(
            model_name="glucose",
            name="glucose_fasting_duration_str",
            field=models.CharField(
                blank=True,
                help_text="As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc",
                max_length=8,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long have they fasted in hours and/or minutes?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsins",
            name="fasting_duration_str",
            field=models.CharField(
                blank=True,
                help_text="As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc",
                max_length=8,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long have they fasted in hours and/or minutes?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="care_visit_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FFACTIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How much time did you spend during your visit today -- from arrival to this place until the end of your visit?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="travel_time",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FTRATIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long did it take you to reach here?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="wait_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FWAITIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How much time did you spend waiting?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="with_hcw_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FWORKTIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How much time did you spend with the healthcare worker?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekingb",
            name="care_visit_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="in hours and minutes (format HH:MM)",
                max_length=5,
                metadata="FOUTTIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="Roughly how much time did you spend during your last/most recent visit?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekingb",
            name="travel_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="in hours and minutes (format HH:MM)",
                max_length=5,
                metadata="FOUTTRATIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long did it take you to get there?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldminitialreview",
            name="glucose_fasting_duration_str",
            field=models.CharField(
                blank=True,
                help_text="As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc",
                max_length=8,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long did they fast (in hours and minutes)?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldmreview",
            name="glucose_fasting_duration_str",
            field=models.CharField(
                blank=True,
                help_text="As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc",
                max_length=8,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long have they fasted in hours and/or minutes?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalglucose",
            name="glucose_fasting_duration_str",
            field=models.CharField(
                blank=True,
                help_text="As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc",
                max_length=8,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long have they fasted in hours and/or minutes?",
            ),
        ),
    ]
