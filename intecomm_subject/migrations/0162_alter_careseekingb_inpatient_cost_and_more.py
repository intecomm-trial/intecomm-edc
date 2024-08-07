# Generated by Django 5.0.4 on 2024-04-10 22:05

import django.core.validators
import edc_model_fields.fields.custom_django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_lists", "0012_visitreasons_custom_name"),
        (
            "intecomm_subject",
            "0161_rename_inpatient_accompany_nowork_careseekingb_inpatient_household_nowork_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="careseekingb",
            name="inpatient_cost",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                help_text="in local currency",
                metadata="FINCOST1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="How much was spent in total on your hospital stay?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekingb",
            name="inpatient_food_cost",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                help_text="in local currency",
                metadata="FINFOODCOST1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="How much was spent on this food and drink?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekingb",
            name="inpatient_household_nowork_days",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                metadata="FINODAYSMISS1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(90),
                ],
                verbose_name="How many days did they not go to work?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekingb",
            name="inpatient_money_sources",
            field=edc_model_fields.fields.custom_django_fields.ManyToManyField2(
                blank=True,
                help_text="Select up to three sources. If 'other', please specify.",
                metadata="FINSOURCE",
                related_name="%(app_label)s_inpatient_money_sources_related",
                related_query_name="%(app_label)s_inpatient_money_sources",
                to="intecomm_lists.moneysources",
                verbose_name="What were the source(s) of payment for all these expenses for your hospital stay?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekingb",
            name="inpatient_money_sources_main",
            field=edc_model_fields.fields.custom_django_fields.ManyToManyField2(
                blank=True,
                metadata="FINSOURCEMAIN1",
                related_name="%(app_label)s_inpatient_money_sources_main_related",
                related_query_name="%(app_label)s_inpatient_money_main_sources",
                to="intecomm_lists.moneysources",
                verbose_name="Of the various sources that you have just mentioned, what was the main source of payment?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekingb",
            name="inpatient_nowork_days",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                metadata="FINWRKMISS1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(90),
                ],
                verbose_name="When you were ill, how many days were you not able to go to work?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekingb",
            name="inpatient_reasons",
            field=edc_model_fields.fields.custom_django_fields.ManyToManyField2(
                blank=True,
                metadata="FINDAYSCOND1",
                related_name="%(app_label)s_inpatient_reasons_related",
                related_query_name="%(app_label)s_inpatient_reasons_sources",
                to="intecomm_lists.conditions",
                verbose_name="What was this INPATIENT care for?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekingb",
            name="inpatient_cost",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                help_text="in local currency",
                metadata="FINCOST1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="How much was spent in total on your hospital stay?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekingb",
            name="inpatient_food_cost",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                help_text="in local currency",
                metadata="FINFOODCOST1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="How much was spent on this food and drink?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekingb",
            name="inpatient_household_nowork_days",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                metadata="FINODAYSMISS1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(90),
                ],
                verbose_name="How many days did they not go to work?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekingb",
            name="inpatient_nowork_days",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                metadata="FINWRKMISS1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(90),
                ],
                verbose_name="When you were ill, how many days were you not able to go to work?",
            ),
        ),
    ]
