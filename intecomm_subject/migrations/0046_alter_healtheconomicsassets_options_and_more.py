# Generated by Django 4.2.1 on 2023-05-24 01:42

from django.db import migrations, models
import edc_model_fields.fields.other_charfield


class Migration(migrations.Migration):
    dependencies = [
        (
            "intecomm_subject",
            "0045_healtheconomicshouseholdhead_hoh_marital_status_other_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="healtheconomicsassets",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Health Economics: Assets",
                "verbose_name_plural": "Health Economics: Assets",
            },
        ),
        migrations.AlterModelOptions(
            name="healtheconomicshouseholdhead",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Health Economics: Household head",
                "verbose_name_plural": "Health Economics: Household head",
            },
        ),
        migrations.AlterModelOptions(
            name="healtheconomicsincome",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Health Economics: Income",
                "verbose_name_plural": "Health Economics: Income",
            },
        ),
        migrations.AlterModelOptions(
            name="healtheconomicspatient",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Health Economics: Patient",
                "verbose_name_plural": "Health Economics: Patient",
            },
        ),
        migrations.AlterModelOptions(
            name="healtheconomicsproperty",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Health Economics: Property",
                "verbose_name_plural": "Health Economics: Property",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalhealtheconomicsassets",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Health Economics: Assets",
                "verbose_name_plural": "historical Health Economics: Assets",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalhealtheconomicshouseholdhead",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Health Economics: Household head",
                "verbose_name_plural": "historical Health Economics: Household head",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalhealtheconomicsincome",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Health Economics: Income",
                "verbose_name_plural": "historical Health Economics: Income",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalhealtheconomicspatient",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Health Economics: Patient",
                "verbose_name_plural": "historical Health Economics: Patient",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalhealtheconomicsproperty",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Health Economics: Property",
                "verbose_name_plural": "historical Health Economics: Property",
            },
        ),
        migrations.AddField(
            model_name="healtheconomicspatient",
            name="pat_education_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If OTHER level of education, specify ...",
            ),
        ),
        migrations.AddField(
            model_name="healtheconomicspatient",
            name="pat_ethnicity_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If OTHER ethnic background, specify ...",
            ),
        ),
        migrations.AddField(
            model_name="healtheconomicspatient",
            name="pat_insurance_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If OTHER health insurance status, specify ...",
            ),
        ),
        migrations.AddField(
            model_name="healtheconomicspatient",
            name="pat_marital_status_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If OTHER marital status, specify ...",
            ),
        ),
        migrations.AddField(
            model_name="healtheconomicspatient",
            name="pat_religion_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If OTHER religious orientation, specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomicspatient",
            name="pat_education_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If OTHER level of education, specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomicspatient",
            name="pat_ethnicity_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If OTHER ethnic background, specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomicspatient",
            name="pat_insurance_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If OTHER health insurance status, specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomicspatient",
            name="pat_marital_status_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If OTHER marital status, specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomicspatient",
            name="pat_religion_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If OTHER religious orientation, specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicsassets",
            name="residence_ownership",
            field=models.CharField(
                choices=[
                    ("renter", "Rent"),
                    ("owner", "Own themselves"),
                    ("family_owned", "Owned by someone else in family"),
                    ("nonfamily_owned", "Owned by someone else other than family member"),
                    ("joint_owned", "Owned together with someone"),
                ],
                max_length=25,
                verbose_name="Is the house you live in rented, owned by you (either on your own, or with someone else), or owned by someone else in your family?",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicshouseholdhead",
            name="hoh_employment",
            field=models.CharField(
                choices=[
                    ("1", "Full time employed"),
                    ("2", "Regular part time employed "),
                    ("3", "Irregular/ occasional/ day worker employment"),
                    ("4", "Non-paid/ voluntary role "),
                    ("5", "Student"),
                    ("6", "Homemaker"),
                    ("7", "Unemployed (able to work)"),
                    ("8", "Unemployed (unable to work)"),
                    ("dont_know", "Don’t know"),
                    ("N/A", "Not applcable"),
                ],
                max_length=25,
                verbose_name="Household head’s employment status",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicshouseholdhead",
            name="hoh_employment_type",
            field=models.CharField(
                choices=[
                    ("1", "Legislators, administrators, and managers"),
                    ("2", "Professionals"),
                    ("3", "Technicians and associate professionals"),
                    ("4", "Clerks"),
                    ("5", "Service workers and shop sale workers"),
                    ("6", "Skilled agricultural and fishery workers"),
                    ("7", "Unskilled agricultural and fishery workers"),
                    ("8", "Craft and related workers"),
                    ("9", "Plant and machine operators and assemblers"),
                    ("10", "Elementary occupations"),
                    ("dont_know", "Don’t know"),
                    ("N/A", "Not applicable"),
                ],
                max_length=25,
                verbose_name="Household head’s type of employment",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicshouseholdhead",
            name="hoh_marital_status",
            field=models.CharField(
                choices=[
                    ("1", "Never Married (but not co-habiting)"),
                    ("2", "Co-habiting"),
                    ("3", "Currently Married"),
                    ("4", "Separated/Divorced"),
                    ("5", "Widowed"),
                    ("OTHER", "Other, specify ..."),
                    ("dont_know", "Don’t know"),
                    ("N/A", "Not applicable"),
                ],
                max_length=25,
                verbose_name="Household head’s marital status",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicspatient",
            name="pat_employment",
            field=models.CharField(
                choices=[
                    ("1", "Full time employed"),
                    ("2", "Regular part time employed "),
                    ("3", "Irregular/ occasional/ day worker employment"),
                    ("4", "Non-paid/ voluntary role "),
                    ("5", "Student"),
                    ("6", "Homemaker"),
                    ("7", "Unemployed (able to work)"),
                    ("8", "Unemployed (unable to work)"),
                    ("dont_know", "Don’t know"),
                    ("N/A", "Not applcable"),
                ],
                max_length=25,
                verbose_name="What is your employment status?",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicspatient",
            name="pat_employment_type",
            field=models.CharField(
                choices=[
                    ("1", "Legislators, administrators, and managers"),
                    ("2", "Professionals"),
                    ("3", "Technicians and associate professionals"),
                    ("4", "Clerks"),
                    ("5", "Service workers and shop sale workers"),
                    ("6", "Skilled agricultural and fishery workers"),
                    ("7", "Unskilled agricultural and fishery workers"),
                    ("8", "Craft and related workers"),
                    ("9", "Plant and machine operators and assemblers"),
                    ("10", "Elementary occupations"),
                    ("dont_know", "Don’t know"),
                    ("N/A", "Not applicable"),
                ],
                max_length=25,
                verbose_name="What is your type of employment?",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicspatient",
            name="pat_marital_status",
            field=models.CharField(
                choices=[
                    ("1", "Never Married (but not co-habiting)"),
                    ("2", "Co-habiting"),
                    ("3", "Currently Married"),
                    ("4", "Separated/Divorced"),
                    ("5", "Widowed"),
                    ("OTHER", "Other, specify ..."),
                    ("dont_know", "Don’t know"),
                    ("N/A", "Not applicable"),
                ],
                max_length=25,
                verbose_name="What is your marital status?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicsassets",
            name="residence_ownership",
            field=models.CharField(
                choices=[
                    ("renter", "Rent"),
                    ("owner", "Own themselves"),
                    ("family_owned", "Owned by someone else in family"),
                    ("nonfamily_owned", "Owned by someone else other than family member"),
                    ("joint_owned", "Owned together with someone"),
                ],
                max_length=25,
                verbose_name="Is the house you live in rented, owned by you (either on your own, or with someone else), or owned by someone else in your family?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicshouseholdhead",
            name="hoh_employment",
            field=models.CharField(
                choices=[
                    ("1", "Full time employed"),
                    ("2", "Regular part time employed "),
                    ("3", "Irregular/ occasional/ day worker employment"),
                    ("4", "Non-paid/ voluntary role "),
                    ("5", "Student"),
                    ("6", "Homemaker"),
                    ("7", "Unemployed (able to work)"),
                    ("8", "Unemployed (unable to work)"),
                    ("dont_know", "Don’t know"),
                    ("N/A", "Not applcable"),
                ],
                max_length=25,
                verbose_name="Household head’s employment status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicshouseholdhead",
            name="hoh_employment_type",
            field=models.CharField(
                choices=[
                    ("1", "Legislators, administrators, and managers"),
                    ("2", "Professionals"),
                    ("3", "Technicians and associate professionals"),
                    ("4", "Clerks"),
                    ("5", "Service workers and shop sale workers"),
                    ("6", "Skilled agricultural and fishery workers"),
                    ("7", "Unskilled agricultural and fishery workers"),
                    ("8", "Craft and related workers"),
                    ("9", "Plant and machine operators and assemblers"),
                    ("10", "Elementary occupations"),
                    ("dont_know", "Don’t know"),
                    ("N/A", "Not applicable"),
                ],
                max_length=25,
                verbose_name="Household head’s type of employment",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicshouseholdhead",
            name="hoh_marital_status",
            field=models.CharField(
                choices=[
                    ("1", "Never Married (but not co-habiting)"),
                    ("2", "Co-habiting"),
                    ("3", "Currently Married"),
                    ("4", "Separated/Divorced"),
                    ("5", "Widowed"),
                    ("OTHER", "Other, specify ..."),
                    ("dont_know", "Don’t know"),
                    ("N/A", "Not applicable"),
                ],
                max_length=25,
                verbose_name="Household head’s marital status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicspatient",
            name="pat_employment",
            field=models.CharField(
                choices=[
                    ("1", "Full time employed"),
                    ("2", "Regular part time employed "),
                    ("3", "Irregular/ occasional/ day worker employment"),
                    ("4", "Non-paid/ voluntary role "),
                    ("5", "Student"),
                    ("6", "Homemaker"),
                    ("7", "Unemployed (able to work)"),
                    ("8", "Unemployed (unable to work)"),
                    ("dont_know", "Don’t know"),
                    ("N/A", "Not applcable"),
                ],
                max_length=25,
                verbose_name="What is your employment status?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicspatient",
            name="pat_employment_type",
            field=models.CharField(
                choices=[
                    ("1", "Legislators, administrators, and managers"),
                    ("2", "Professionals"),
                    ("3", "Technicians and associate professionals"),
                    ("4", "Clerks"),
                    ("5", "Service workers and shop sale workers"),
                    ("6", "Skilled agricultural and fishery workers"),
                    ("7", "Unskilled agricultural and fishery workers"),
                    ("8", "Craft and related workers"),
                    ("9", "Plant and machine operators and assemblers"),
                    ("10", "Elementary occupations"),
                    ("dont_know", "Don’t know"),
                    ("N/A", "Not applicable"),
                ],
                max_length=25,
                verbose_name="What is your type of employment?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicspatient",
            name="pat_marital_status",
            field=models.CharField(
                choices=[
                    ("1", "Never Married (but not co-habiting)"),
                    ("2", "Co-habiting"),
                    ("3", "Currently Married"),
                    ("4", "Separated/Divorced"),
                    ("5", "Widowed"),
                    ("OTHER", "Other, specify ..."),
                    ("dont_know", "Don’t know"),
                    ("N/A", "Not applicable"),
                ],
                max_length=25,
                verbose_name="What is your marital status?",
            ),
        ),
    ]
