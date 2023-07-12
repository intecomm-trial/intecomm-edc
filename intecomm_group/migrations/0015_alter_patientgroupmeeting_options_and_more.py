# Generated by Django 4.2.1 on 2023-07-06 02:18

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import edc_sites.model_mixins


class Migration(migrations.Migration):
    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("intecomm_group", "0014_alter_communitycarelocation_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="patientgroupmeeting",
            options={
                "default_manager_name": "objects",
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Patient Group Meeting",
                "verbose_name_plural": "Patient Groups Meeting",
            },
        ),
        migrations.AlterModelManagers(
            name="patientgroupappointment",
            managers=[
                ("on_site", edc_sites.model_mixins.CurrentSiteManager()),
                ("objects", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="patientgroupmeeting",
            managers=[
                ("on_site", edc_sites.model_mixins.CurrentSiteManager()),
                ("objects", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name="patientgroupappointment",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.site",
            ),
        ),
        migrations.AddField(
            model_name="patientgroupmeeting",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.site",
            ),
        ),
    ]