# Generated by Django 4.2.1 on 2023-07-05 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_screening", "0042_alter_healthfacility_options_and_more"),
        (
            "intecomm_subject",
            "0050_alter_healtheconomicshouseholdhead_hoh_ethnicity_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bloodresultsfbc",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Blood Result: FBC",
                "verbose_name_plural": "Blood Results: FBC",
            },
        ),
        migrations.AlterModelOptions(
            name="bloodresultsglu",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Blood Result: Glucose",
                "verbose_name_plural": "Blood Results: Glucose",
            },
        ),
        migrations.AlterModelOptions(
            name="bloodresultshba1c",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Blood Result: HbA1c",
                "verbose_name_plural": "Blood Results: HbA1c",
            },
        ),
        migrations.AlterModelOptions(
            name="bloodresultsins",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Blood Result: Insulin",
                "verbose_name_plural": "Blood Results: Insulin",
            },
        ),
        migrations.AlterModelOptions(
            name="bloodresultslft",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Blood Result: LFT",
                "verbose_name_plural": "Blood Results: LFT",
            },
        ),
        migrations.AlterModelOptions(
            name="bloodresultslipid",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Blood Result: Lipids",
                "verbose_name_plural": "Blood Results: Lipids",
            },
        ),
        migrations.AlterModelOptions(
            name="bloodresultsrft",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Blood Result: RFT",
                "verbose_name_plural": "Blood Results: RFT",
            },
        ),
        migrations.AlterModelOptions(
            name="cd4result",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "CD4 Result",
                "verbose_name_plural": "CD4 Results",
            },
        ),
        migrations.AlterModelOptions(
            name="clinicalreview",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Clinical Review",
                "verbose_name_plural": "Clinical Reviews",
            },
        ),
        migrations.AlterModelOptions(
            name="clinicalreviewbaseline",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Clinical Review: Baseline",
                "verbose_name_plural": "Clinical Review: Baseline",
            },
        ),
        migrations.AlterModelOptions(
            name="complicationsbaseline",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Complications: Baseline",
                "verbose_name_plural": "Complications: Baseline",
            },
        ),
        migrations.AlterModelOptions(
            name="complicationsfollowup",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Complications: Followup",
                "verbose_name_plural": "Complications: Followup",
            },
        ),
        migrations.AlterModelOptions(
            name="concomitantmedication",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Concomitant Medication",
                "verbose_name_plural": "Concomitant Medication",
            },
        ),
        migrations.AlterModelOptions(
            name="dminitialreview",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Diabetes Initial Review",
                "verbose_name_plural": "Diabetes Initial Reviews",
            },
        ),
        migrations.AlterModelOptions(
            name="dmmedicationadherence",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Medication Adherence (Diabetes)",
                "verbose_name_plural": "Medication Adherence (Diabetes)",
            },
        ),
        migrations.AlterModelOptions(
            name="dmreview",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Diabetes Review",
                "verbose_name_plural": "Diabetes Review",
            },
        ),
        migrations.AlterModelOptions(
            name="drugrefilldm",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Drug Refill: Diabetes",
                "verbose_name_plural": "Drug Refills: Diabetes",
            },
        ),
        migrations.AlterModelOptions(
            name="drugrefillhiv",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Drug Refill: HIV",
                "verbose_name_plural": "Drug Refills: HIV",
            },
        ),
        migrations.AlterModelOptions(
            name="drugrefillhtn",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Drug Refill: Hypertension",
                "verbose_name_plural": "Drug Refills: Hypertension",
            },
        ),
        migrations.AlterModelOptions(
            name="drugsupplydm",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Drug Supply: Diabetes",
                "verbose_name_plural": "Drug Supply: Diabetes",
            },
        ),
        migrations.AlterModelOptions(
            name="drugsupplyhiv",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Drug Supply: HIV",
                "verbose_name_plural": "Drug Supply: HIV",
            },
        ),
        migrations.AlterModelOptions(
            name="drugsupplyhtn",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Drug Supply: Hypertension",
                "verbose_name_plural": "Drug Supply: Hypertension",
            },
        ),
        migrations.AlterModelOptions(
            name="eq5d3l",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "EuroQol EQ-5D-3L Instrument",
                "verbose_name_plural": "EuroQol EQ-5D-3L Instrument",
            },
        ),
        migrations.AlterModelOptions(
            name="familyhistory",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Family History and Knowledge",
                "verbose_name_plural": "Family History and Knowledge",
            },
        ),
        migrations.AlterModelOptions(
            name="glucose",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Glucose",
                "verbose_name_plural": "Glucose",
            },
        ),
        migrations.AlterModelOptions(
            name="hba1cresult",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "HbA1c Result",
                "verbose_name_plural": "HbA1c Results",
            },
        ),
        migrations.AlterModelOptions(
            name="healtheconomics",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Health Economics",
                "verbose_name_plural": "Health Economics",
            },
        ),
        migrations.AlterModelOptions(
            name="healtheconomicsassets",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Health Economics: Assets",
                "verbose_name_plural": "Health Economics: Assets",
            },
        ),
        migrations.AlterModelOptions(
            name="healtheconomicshouseholdhead",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Health Economics: Household head",
                "verbose_name_plural": "Health Economics: Household head",
            },
        ),
        migrations.AlterModelOptions(
            name="healtheconomicsincome",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Health Economics: Income",
                "verbose_name_plural": "Health Economics: Income",
            },
        ),
        migrations.AlterModelOptions(
            name="healtheconomicspatient",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Health Economics: Patient",
                "verbose_name_plural": "Health Economics: Patient",
            },
        ),
        migrations.AlterModelOptions(
            name="healtheconomicsproperty",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Health Economics: Property",
                "verbose_name_plural": "Health Economics: Property",
            },
        ),
        migrations.AlterModelOptions(
            name="hivinitialreview",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "HIV Initial Review",
                "verbose_name_plural": "HIV Initial Reviews",
            },
        ),
        migrations.AlterModelOptions(
            name="hivmedicationadherence",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Medication Adherence (HIV)",
                "verbose_name_plural": "Medication Adherence (HIV)",
            },
        ),
        migrations.AlterModelOptions(
            name="hivreview",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "HIV Review",
                "verbose_name_plural": "HIV Review",
            },
        ),
        migrations.AlterModelOptions(
            name="htninitialreview",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Hypertension Initial Review",
                "verbose_name_plural": "Hypertension Initial Reviews",
            },
        ),
        migrations.AlterModelOptions(
            name="htnmedicationadherence",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Medication Adherence (Hypertension)",
                "verbose_name_plural": "Medication Adherence (Hypertension)",
            },
        ),
        migrations.AlterModelOptions(
            name="htnreview",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Hypertension Review",
                "verbose_name_plural": "Hypertension Review",
            },
        ),
        migrations.AlterModelOptions(
            name="icecapa",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Overall quality of life (ICECAP-A V2)",
                "verbose_name_plural": "Overall quality of life (ICECAP-A V2)",
            },
        ),
        migrations.AlterModelOptions(
            name="investigations",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Investigations",
                "verbose_name_plural": "Investigations",
            },
        ),
        migrations.AlterModelOptions(
            name="malariatest",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Malaria Test",
            },
        ),
        migrations.AlterModelOptions(
            name="medications",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Medications",
                "verbose_name_plural": "Medications",
            },
        ),
        migrations.AlterModelOptions(
            name="nextappointment",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Next Appointment",
                "verbose_name_plural": "Next Appointments",
            },
        ),
        migrations.AlterModelOptions(
            name="otherbaselinedata",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Other Baseline Data",
                "verbose_name_plural": "Other Baseline Data",
            },
        ),
        migrations.AlterModelOptions(
            name="socialharms",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Social Harms",
                "verbose_name_plural": "Social Harms",
            },
        ),
        migrations.AlterModelOptions(
            name="subjectrequisition",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
            },
        ),
        migrations.AlterModelOptions(
            name="subjectvisit",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": (
                    "subject_identifier",
                    "visit_schedule_name",
                    "schedule_name",
                    "visit_code",
                    "visit_code_sequence",
                    "report_datetime",
                ),
            },
        ),
        migrations.AlterModelOptions(
            name="subjectvisitmissed",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Missed Visit Report",
                "verbose_name_plural": "Missed Visit Report",
            },
        ),
        migrations.AlterModelOptions(
            name="urinedipsticktest",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Urine Dipstick Test",
            },
        ),
        migrations.AlterModelOptions(
            name="urinepregnancy",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Urine Pregnancy",
            },
        ),
        migrations.AlterModelOptions(
            name="viralloadresult",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Viral Load Result",
                "verbose_name_plural": "Viral Load Results",
            },
        ),
        migrations.AlterModelOptions(
            name="vitals",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Vitals",
                "verbose_name_plural": "Vitals",
            },
        ),
        migrations.AlterField(
            model_name="healtheconomicsassets",
            name="window_screen_type",
            field=models.CharField(
                choices=[
                    ("1", "Wire mesh"),
                    ("2", "Old bednet"),
                    ("3", "No windows screened"),
                    ("4", "No windows"),
                    ("N/A", "Not applicable"),
                ],
                max_length=25,
                verbose_name="Type of screening on external windows",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicsassets",
            name="window_screens",
            field=models.CharField(
                choices=[
                    ("1", "All windows screened"),
                    ("2", "No windows screened"),
                    ("2", "Some windows screened"),
                ],
                max_length=25,
                verbose_name="What is the main screening material of external windows?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicsassets",
            name="window_screen_type",
            field=models.CharField(
                choices=[
                    ("1", "Wire mesh"),
                    ("2", "Old bednet"),
                    ("3", "No windows screened"),
                    ("4", "No windows"),
                    ("N/A", "Not applicable"),
                ],
                max_length=25,
                verbose_name="Type of screening on external windows",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicsassets",
            name="window_screens",
            field=models.CharField(
                choices=[
                    ("1", "All windows screened"),
                    ("2", "No windows screened"),
                    ("2", "Some windows screened"),
                ],
                max_length=25,
                verbose_name="What is the main screening material of external windows?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalnextappointment",
            name="health_facility",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="intecomm_screening.healthfacility",
            ),
        ),
        migrations.AlterField(
            model_name="nextappointment",
            name="health_facility",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="intecomm_screening.healthfacility",
            ),
        ),
    ]
