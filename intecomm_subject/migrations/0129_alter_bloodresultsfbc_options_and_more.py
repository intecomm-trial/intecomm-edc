# Generated by Django 4.2.7 on 2023-12-04 22:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "intecomm_subject",
            "0128_remove_historicalsubjectvisit_clinic_services_other_and_more",
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
                "verbose_name": "CD4 Result",
                "verbose_name_plural": "CD4 Results",
            },
        ),
        migrations.AlterModelOptions(
            name="clinicalnote",
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
                "verbose_name": "Clinical Note",
                "verbose_name_plural": "Clinical Note",
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
                "verbose_name": "Glucose",
                "verbose_name_plural": "Glucose",
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
                "verbose_name": "Overall quality of life (ICECAP-A V2)",
                "verbose_name_plural": "Overall quality of life (ICECAP-A V2)",
            },
        ),
        migrations.AlterModelOptions(
            name="locationupdate",
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
                "verbose_name": "Location update",
                "verbose_name_plural": "Location updates",
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
                "verbose_name": "Malaria Test",
                "verbose_name_plural": "Malaria Tests",
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
                "verbose_name": "Subject requisition",
                "verbose_name_plural": "Subject requisitions",
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
                "verbose_name": "Subject visit",
                "verbose_name_plural": "Subject visits",
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
                "verbose_name": "Urine dipstick test",
                "verbose_name_plural": "Urine dipstick tests",
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
                "verbose_name": "Urine pregnancy test",
                "verbose_name_plural": "Urine pregnancy tests",
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
                "verbose_name": "Vitals",
                "verbose_name_plural": "Vitals",
            },
        ),
    ]
