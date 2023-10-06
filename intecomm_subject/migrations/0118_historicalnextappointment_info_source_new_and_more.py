# Generated by Django 4.2.5 on 2023-10-05 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("edc_appointment", "0046_infosources"),
        ("intecomm_subject", "0117_historicalnextappointment_allow_create_interim_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalnextappointment",
            name="info_source_new",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                max_length=15,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_appointment.infosources",
                verbose_name="What is the source of this appointment date",
            ),
        ),
        migrations.AddField(
            model_name="nextappointment",
            name="info_source_new",
            field=models.ForeignKey(
                max_length=15,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_appointment.infosources",
                verbose_name="What is the source of this appointment date",
            ),
        ),
    ]
