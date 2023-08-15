# Generated by Django 4.2.3 on 2023-08-15 01:45

from django.db import migrations, models
import django.db.models.deletion
import edc_model_fields.fields.other_charfield


class Migration(migrations.Migration):
    dependencies = [
        ("edc_adverse_event", "0012_aeactionclassification_extra_value_and_more"),
        ("intecomm_ae", "0006_hospitalization_historicalhospitalization"),
    ]

    operations = [
        migrations.AddField(
            model_name="aeinitial",
            name="ae_classification_as_text",
            field=models.CharField(
                help_text="Keep this simple. Provide details below",
                max_length=150,
                null=True,
                verbose_name="Adverse Event (AE) Classification",
            ),
        ),
        migrations.AddField(
            model_name="historicalaeinitial",
            name="ae_classification_as_text",
            field=models.CharField(
                help_text="Keep this simple. Provide details below",
                max_length=150,
                null=True,
                verbose_name="Adverse Event (AE) Classification",
            ),
        ),
        migrations.AlterField(
            model_name="aeinitial",
            name="ae_classification",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_adverse_event.aeclassification",
                verbose_name="Adverse Event (AE) Classification",
            ),
        ),
        migrations.AlterField(
            model_name="aeinitial",
            name="ae_classification_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                editable=False,
                max_length=250,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="historicalaeinitial",
            name="ae_classification",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_adverse_event.aeclassification",
                verbose_name="Adverse Event (AE) Classification",
            ),
        ),
        migrations.AlterField(
            model_name="historicalaeinitial",
            name="ae_classification_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                editable=False,
                max_length=250,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
    ]
