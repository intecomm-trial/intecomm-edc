# Generated by Django 4.2.7 on 2023-12-05 20:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0132_alter_subjectrequisition_unique_together_and_more"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="bloodresultsfbc",
            index=models.Index(
                fields=["subject_visit", "site"], name="intecomm_su_subject_3bd165_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultsfbc",
            index=models.Index(
                fields=["modified", "created"], name="intecomm_su_modifie_4b24dd_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultsfbc",
            index=models.Index(
                fields=["user_modified", "user_created"], name="intecomm_su_user_mo_263115_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultsglu",
            index=models.Index(
                fields=["subject_visit", "site"], name="intecomm_su_subject_eb429a_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultsglu",
            index=models.Index(
                fields=["modified", "created"], name="intecomm_su_modifie_ac7e13_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultsglu",
            index=models.Index(
                fields=["user_modified", "user_created"], name="intecomm_su_user_mo_e3b982_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultshba1c",
            index=models.Index(
                fields=["subject_visit", "site"], name="intecomm_su_subject_2983d9_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultshba1c",
            index=models.Index(
                fields=["modified", "created"], name="intecomm_su_modifie_b05d6d_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultshba1c",
            index=models.Index(
                fields=["user_modified", "user_created"], name="intecomm_su_user_mo_c6051a_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultsins",
            index=models.Index(
                fields=["subject_visit", "site"], name="intecomm_su_subject_01a47a_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultsins",
            index=models.Index(
                fields=["modified", "created"], name="intecomm_su_modifie_341708_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultsins",
            index=models.Index(
                fields=["user_modified", "user_created"], name="intecomm_su_user_mo_dffdda_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultslft",
            index=models.Index(
                fields=["subject_visit", "site"], name="intecomm_su_subject_df2b7f_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultslft",
            index=models.Index(
                fields=["modified", "created"], name="intecomm_su_modifie_18c09e_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultslft",
            index=models.Index(
                fields=["user_modified", "user_created"], name="intecomm_su_user_mo_b12c36_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultslipid",
            index=models.Index(
                fields=["subject_visit", "site"], name="intecomm_su_subject_0dd0d1_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultslipid",
            index=models.Index(
                fields=["modified", "created"], name="intecomm_su_modifie_2deb12_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultslipid",
            index=models.Index(
                fields=["user_modified", "user_created"], name="intecomm_su_user_mo_4870e2_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultsrft",
            index=models.Index(
                fields=["subject_visit", "site"], name="intecomm_su_subject_7bc0b6_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultsrft",
            index=models.Index(
                fields=["modified", "created"], name="intecomm_su_modifie_c1e6b4_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultsrft",
            index=models.Index(
                fields=["user_modified", "user_created"], name="intecomm_su_user_mo_3922a4_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="cd4result",
            index=models.Index(
                fields=["subject_visit", "site"], name="intecomm_su_subject_a40fc4_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="cd4result",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="intecomm_su_subject_85e709_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="cd4result",
            index=models.Index(
                fields=["modified", "created"], name="intecomm_su_modifie_9f8432_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="cd4result",
            index=models.Index(
                fields=["user_modified", "user_created"], name="intecomm_su_user_mo_a8ac98_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="clinicalnote",
            index=models.Index(
                fields=["subject_visit", "site"], name="intecomm_su_subject_193cc0_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="clinicalnote",
            index=models.Index(
                fields=["modified", "created"], name="intecomm_su_modifie_1e0564_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="clinicalnote",
            index=models.Index(
                fields=["user_modified", "user_created"], name="intecomm_su_user_mo_81a993_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="clinicalreview",
            index=models.Index(
                fields=["subject_visit", "site"], name="intecomm_su_subject_c37967_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="clinicalreview",
            index=models.Index(
                fields=["modified", "created"], name="intecomm_su_modifie_e40016_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="clinicalreview",
            index=models.Index(
                fields=["user_modified", "user_created"], name="intecomm_su_user_mo_3f082b_idx"
            ),
        ),
    ]
