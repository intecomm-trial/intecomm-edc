# Generated by Django 4.1.7 on 2023-04-17 18:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "intecomm_subject",
            "0027_dminitialreview_rx_init_dminitialreview_rx_init_date_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="clinicalreviewbaseline",
            name="dm_test",
        ),
        migrations.RemoveField(
            model_name="clinicalreviewbaseline",
            name="dm_test_ago",
        ),
        migrations.RemoveField(
            model_name="clinicalreviewbaseline",
            name="dm_test_date",
        ),
        migrations.RemoveField(
            model_name="clinicalreviewbaseline",
            name="dm_test_estimated_date",
        ),
        migrations.RemoveField(
            model_name="clinicalreviewbaseline",
            name="hiv_test",
        ),
        migrations.RemoveField(
            model_name="clinicalreviewbaseline",
            name="hiv_test_ago",
        ),
        migrations.RemoveField(
            model_name="clinicalreviewbaseline",
            name="hiv_test_date",
        ),
        migrations.RemoveField(
            model_name="clinicalreviewbaseline",
            name="hiv_test_estimated_date",
        ),
        migrations.RemoveField(
            model_name="clinicalreviewbaseline",
            name="htn_test",
        ),
        migrations.RemoveField(
            model_name="clinicalreviewbaseline",
            name="htn_test_ago",
        ),
        migrations.RemoveField(
            model_name="clinicalreviewbaseline",
            name="htn_test_date",
        ),
        migrations.RemoveField(
            model_name="clinicalreviewbaseline",
            name="htn_test_estimated_date",
        ),
        migrations.RemoveField(
            model_name="historicalclinicalreviewbaseline",
            name="dm_test",
        ),
        migrations.RemoveField(
            model_name="historicalclinicalreviewbaseline",
            name="dm_test_ago",
        ),
        migrations.RemoveField(
            model_name="historicalclinicalreviewbaseline",
            name="dm_test_date",
        ),
        migrations.RemoveField(
            model_name="historicalclinicalreviewbaseline",
            name="dm_test_estimated_date",
        ),
        migrations.RemoveField(
            model_name="historicalclinicalreviewbaseline",
            name="hiv_test",
        ),
        migrations.RemoveField(
            model_name="historicalclinicalreviewbaseline",
            name="hiv_test_ago",
        ),
        migrations.RemoveField(
            model_name="historicalclinicalreviewbaseline",
            name="hiv_test_date",
        ),
        migrations.RemoveField(
            model_name="historicalclinicalreviewbaseline",
            name="hiv_test_estimated_date",
        ),
        migrations.RemoveField(
            model_name="historicalclinicalreviewbaseline",
            name="htn_test",
        ),
        migrations.RemoveField(
            model_name="historicalclinicalreviewbaseline",
            name="htn_test_ago",
        ),
        migrations.RemoveField(
            model_name="historicalclinicalreviewbaseline",
            name="htn_test_date",
        ),
        migrations.RemoveField(
            model_name="historicalclinicalreviewbaseline",
            name="htn_test_estimated_date",
        ),
        migrations.AlterField(
            model_name="clinicalreviewbaseline",
            name="dm_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="Has the patient ever been diagnosed with Diabetes",
            ),
        ),
        migrations.AlterField(
            model_name="clinicalreviewbaseline",
            name="hiv_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
            ),
        ),
        migrations.AlterField(
            model_name="clinicalreviewbaseline",
            name="htn_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="Has the patient ever been diagnosed with Hypertension",
            ),
        ),
        migrations.AlterField(
            model_name="historicalclinicalreviewbaseline",
            name="dm_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="Has the patient ever been diagnosed with Diabetes",
            ),
        ),
        migrations.AlterField(
            model_name="historicalclinicalreviewbaseline",
            name="hiv_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
            ),
        ),
        migrations.AlterField(
            model_name="historicalclinicalreviewbaseline",
            name="htn_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="Has the patient ever been diagnosed with Hypertension",
            ),
        ),
    ]
