# Generated by Django 4.2.3 on 2023-07-17 14:37

import django.core.validators
from django.db import migrations, models
import edc_model_fields.fields.other_charfield


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0056_alter_drugrefilldm_rx_days_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalotherbaselinedata",
            old_name="smoker_current_duration",
            new_name="smoker_duration",
        ),
        migrations.RenameField(
            model_name="historicalotherbaselinedata",
            old_name="smoker_current_duration_estimated_date",
            new_name="smoker_duration_estimated_date",
        ),
        migrations.RenameField(
            model_name="otherbaselinedata",
            old_name="smoker_current_duration",
            new_name="smoker_duration",
        ),
        migrations.RenameField(
            model_name="otherbaselinedata",
            old_name="smoker_current_duration_estimated_date",
            new_name="smoker_duration_estimated_date",
        ),
        migrations.RemoveField(
            model_name="healtheconomicshouseholdhead",
            name="hoh_citizen",
        ),
        migrations.RemoveField(
            model_name="historicalhealtheconomicshouseholdhead",
            name="hoh_citizen",
        ),
        migrations.AddField(
            model_name="healtheconomicshouseholdhead",
            name="hoh_employment_type_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                help_text="... other type of employment",
                max_length=100,
                null=True,
                verbose_name="Household head’s type of employment",
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomicshouseholdhead",
            name="hoh_employment_type_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                help_text="... other type of employment",
                max_length=100,
                null=True,
                verbose_name="Household head’s type of employment",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicshouseholdhead",
            name="hh_count",
            field=models.IntegerField(
                help_text="Persons",
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(25),
                ],
                verbose_name="What is the total number of people who live in your household?",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicshouseholdhead",
            name="hh_minors_count",
            field=models.IntegerField(
                help_text="Persons",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(25),
                ],
                verbose_name="What is the total number of people 14 years or under who live in your household?",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicshouseholdhead",
            name="relationship_to_hoh",
            field=models.CharField(
                choices=[
                    ("WIFE_HUSBAND", "Wife/Husband"),
                    ("SON_DAUGHTER", "Son/Daughter"),
                    ("SON_DAUGHTERINLAW", "Son/Daughter-in-law"),
                    ("GRANDCHILD", "Grandchild"),
                    ("PARENT", "Parent"),
                    ("PARENTINLAW", "Parent-in-law"),
                    ("BROTHER_SISTER", "Brother/Sister"),
                    ("OTHER", "Other, specify ..."),
                    ("dont_know", "Don’t know"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                help_text="Not applicable if patient is head of household",
                max_length=25,
                verbose_name="What is your relationship to the household head?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicshouseholdhead",
            name="hh_count",
            field=models.IntegerField(
                help_text="Persons",
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(25),
                ],
                verbose_name="What is the total number of people who live in your household?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicshouseholdhead",
            name="hh_minors_count",
            field=models.IntegerField(
                help_text="Persons",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(25),
                ],
                verbose_name="What is the total number of people 14 years or under who live in your household?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicshouseholdhead",
            name="relationship_to_hoh",
            field=models.CharField(
                choices=[
                    ("WIFE_HUSBAND", "Wife/Husband"),
                    ("SON_DAUGHTER", "Son/Daughter"),
                    ("SON_DAUGHTERINLAW", "Son/Daughter-in-law"),
                    ("GRANDCHILD", "Grandchild"),
                    ("PARENT", "Parent"),
                    ("PARENTINLAW", "Parent-in-law"),
                    ("BROTHER_SISTER", "Brother/Sister"),
                    ("OTHER", "Other, specify ..."),
                    ("dont_know", "Don’t know"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                help_text="Not applicable if patient is head of household",
                max_length=25,
                verbose_name="What is your relationship to the household head?",
            ),
        ),
    ]
