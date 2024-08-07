# Generated by Django 4.2.10 on 2024-02-28 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_consent", "0023_alter_subjectconsent_managers"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalsubjectconsent",
            old_name="updates_versions",
            new_name="update_versions",
        ),
        migrations.RenameField(
            model_name="historicalsubjectconsenttz",
            old_name="updates_versions",
            new_name="update_versions",
        ),
        migrations.RenameField(
            model_name="historicalsubjectconsentug",
            old_name="updates_versions",
            new_name="update_versions",
        ),
        migrations.RenameField(
            model_name="subjectconsent",
            old_name="updates_versions",
            new_name="update_versions",
        ),
        migrations.AddField(
            model_name="historicalsubjectconsent",
            name="consent_definition_name",
            field=models.CharField(
                editable=False, max_length=50, null=True, verbose_name="Consent definition"
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectconsenttz",
            name="consent_definition_name",
            field=models.CharField(
                editable=False, max_length=50, null=True, verbose_name="Consent definition"
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectconsentug",
            name="consent_definition_name",
            field=models.CharField(
                editable=False, max_length=50, null=True, verbose_name="Consent definition"
            ),
        ),
        migrations.AddField(
            model_name="subjectconsent",
            name="consent_definition_name",
            field=models.CharField(
                editable=False, max_length=50, null=True, verbose_name="Consent definition"
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="version",
            field=models.CharField(
                editable=False,
                help_text="See 'consent definition' for consent versions by period.",
                max_length=10,
                verbose_name="Consent version",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsenttz",
            name="version",
            field=models.CharField(
                editable=False,
                help_text="See 'consent definition' for consent versions by period.",
                max_length=10,
                verbose_name="Consent version",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentug",
            name="version",
            field=models.CharField(
                editable=False,
                help_text="See 'consent definition' for consent versions by period.",
                max_length=10,
                verbose_name="Consent version",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="version",
            field=models.CharField(
                editable=False,
                help_text="See 'consent definition' for consent versions by period.",
                max_length=10,
                verbose_name="Consent version",
            ),
        ),
    ]
