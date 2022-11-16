# Generated by Django 4.1.2 on 2022-11-16 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import edc_sites.models
import intecomm_screening.models.patient_log


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("intecomm_group", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("intecomm_lists", "0001_initial"),
        ("intecomm_screening", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PatientLog",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("intecomm_screening.patientlog",),
            managers=[
                ("on_site", edc_sites.models.CurrentSiteManager()),
                ("objects", intecomm_screening.models.patient_log.PatientLogManager()),
            ],
        ),
        migrations.AddField(
            model_name="patientgroupmeeting",
            name="patient_group_appointment",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                to="intecomm_group.patientgroupappointment",
            ),
        ),
        migrations.AddField(
            model_name="patientgroupmeeting",
            name="patients",
            field=models.ManyToManyField(
                to="intecomm_screening.patientlog", verbose_name="Attendance"
            ),
        ),
        migrations.AddField(
            model_name="patientgroupappointment",
            name="community_care_location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="intecomm_group.communitycarelocation",
            ),
        ),
        migrations.AddField(
            model_name="patientgroupappointment",
            name="patient_group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="intecomm_group.patientgroup"
            ),
        ),
        migrations.AddField(
            model_name="patientgroup",
            name="patients",
            field=models.ManyToManyField(
                blank=True, to="intecomm_group.patientlog", verbose_name="Membership"
            ),
        ),
        migrations.AddField(
            model_name="patientgroup",
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
            model_name="historicalpatientlog",
            name="history_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="historicalpatientlog",
            name="patient_group",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                help_text="This can be changed at anytime until the group is flagged as COMPLETE. It is recommended to choose a group early in the process.",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="intecomm_screening.patientgroup",
                verbose_name="Choose a group (RECOMMENDED)",
            ),
        ),
        migrations.AddField(
            model_name="historicalpatientlog",
            name="site",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="sites.site",
                verbose_name="Health facility",
            ),
        ),
        migrations.AddField(
            model_name="historicalpatientgroup",
            name="history_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="historicalpatientgroup",
            name="site",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="sites.site",
            ),
        ),
        migrations.AddField(
            model_name="communitycarelocation",
            name="location_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="intecomm_lists.locationtypes"
            ),
        ),
        migrations.AddField(
            model_name="communitycarelocation",
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
