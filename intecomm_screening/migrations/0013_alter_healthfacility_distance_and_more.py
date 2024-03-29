# Generated by Django 4.1.2 on 2022-11-26 03:40

from django.db import migrations, models
import django_crypto_fields.fields.encrypted_char_field


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_screening", "0012_alter_historicalpatientcall_last_attend_clinic_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="healthfacility",
            name="distance",
            field=models.IntegerField(
                help_text="In km. If within the integrated-care clinic facility type '0'",
                verbose_name="Approximate distance from integrated-care clinic",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealthfacility",
            name="distance",
            field=models.IntegerField(
                help_text="In km. If within the integrated-care clinic facility type '0'",
                verbose_name="Approximate distance from integrated-care clinic",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatientlog",
            name="hospital_identifier",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                db_index=True,
                help_text="Must be unique (Encryption: RSA local)",
                max_length=71,
                verbose_name="Hospital identifier",
            ),
        ),
        migrations.AlterField(
            model_name="patientlog",
            name="hospital_identifier",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text="Must be unique (Encryption: RSA local)",
                max_length=71,
                unique=True,
                verbose_name="Hospital identifier",
            ),
        ),
    ]
