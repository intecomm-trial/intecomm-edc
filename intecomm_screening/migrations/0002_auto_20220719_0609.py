# Generated by Django 3.2.14 on 2022-07-19 03:09

import _socket
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.fields.uuid_auto_field
import django_audit_fields.models.audit_model_mixin
import django_crypto_fields.fields.encrypted_char_field
import django_revision.revision_field
import edc_screening.model_mixins.screening_fields_model_mixin
import edc_sites.models
import edc_utils.date
import edc_vitals.models.fields.blood_pressure
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0002_alter_domain_unique'),
        ('intecomm_screening', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScreeningPartOne',
            fields=[
            ],
            options={
                'verbose_name': 'Subject Screening: Part One',
                'verbose_name_plural': 'Subject Screening: Part One',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('intecomm_screening.subjectscreening',),
            managers=[
                ('on_site', edc_sites.models.CurrentSiteManager()),
                ('objects', edc_screening.model_mixins.screening_fields_model_mixin.ScreeningManager()),
            ],
        ),
        migrations.CreateModel(
            name='ScreeningPartTwo',
            fields=[
            ],
            options={
                'verbose_name': 'Subject Screening: Part Two',
                'verbose_name_plural': 'Subject Screening: Part Two',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('intecomm_screening.subjectscreening',),
            managers=[
                ('on_site', edc_sites.models.CurrentSiteManager()),
                ('objects', edc_screening.model_mixins.screening_fields_model_mixin.ScreeningManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='historicalsubjectscreening',
            name='hospital_identifier',
        ),
        migrations.RemoveField(
            model_name='historicalsubjectscreening',
            name='lives_nearby',
        ),
        migrations.RemoveField(
            model_name='historicalsubjectscreening',
            name='staying_nearby_12',
        ),
        migrations.RemoveField(
            model_name='subjectscreening',
            name='hospital_identifier',
        ),
        migrations.RemoveField(
            model_name='subjectscreening',
            name='lives_nearby',
        ),
        migrations.RemoveField(
            model_name='subjectscreening',
            name='staying_nearby_12',
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='appt_datetime',
            field=models.DateTimeField(blank=True, help_text='Leave blank if continuing to the second stage today', null=True, verbose_name='Appointment date for second stage of screening (P2)'),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='continue_part_two',
            field=models.CharField(choices=[('Yes', 'Yes (default)'), ('No', 'No')], default='Yes', help_text='<B>Important</B>: This response will be be automatically set to YES if:<BR><BR>- the participant meets the eligibility criteria for part one, or;<BR><BR>- the eligibility criteria for part two is already complete.<BR>', max_length=15, verbose_name='Continue with <U>part two</U> of the screening process?'),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='dia_blood_pressure',
            field=edc_vitals.models.fields.blood_pressure.DiastolicPressureField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='dia_blood_pressure_avg',
            field=models.IntegerField(blank=True, null=True, verbose_name='Blood pressure: diastolic (average)'),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='dia_blood_pressure_one',
            field=edc_vitals.models.fields.blood_pressure.DiastolicPressureField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='dia_blood_pressure_two',
            field=edc_vitals.models.fields.blood_pressure.DiastolicPressureField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='fasted',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, null=True, verbose_name='Did the patient come to the clinic fasted?'),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='fasting',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='As reported by patient', max_length=15, null=True, verbose_name='Has the participant fasted?'),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='fasting_duration_minutes',
            field=models.IntegerField(help_text='system calculated value', null=True),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='fasting_duration_str',
            field=models.CharField(blank=True, help_text='As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc', max_length=8, null=True, validators=[django.core.validators.RegexValidator('^([0-9]{1,3}h([0-5]?[0-9]m)?)$', message='Invalid format. Expected something like 1h20m, 11h5m, etc')], verbose_name='How long have they fasted in hours and/or minutes?'),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='fbg_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='<u>Time</u> FBG level measured'),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='fbg_quantifier',
            field=models.CharField(choices=[('=', '='), ('>', '>'), ('>=', '>='), ('<', '<'), ('<=', '<=')], default='=', max_length=10, verbose_name='FBG quantifier'),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='fbg_units',
            field=models.CharField(blank=True, choices=[('mg/dL', 'mg/dL'), ('mmol/L', 'mmol/L (millimoles/L)')], max_length=15, null=True, verbose_name='FBG units'),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='fbg_value',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='A `HIGH` reading may be entered as 9999.99', max_digits=8, null=True, verbose_name='FBG level'),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='part_two_report_datetime',
            field=models.DateTimeField(help_text='Date and time of report.', null=True, verbose_name='Part 2 report date and time'),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='patient_conditions',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, null=True, verbose_name='The participant has at least one of the following conditions: HIV, diabetes or hypertension?'),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='severe_htn',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], help_text='Based on the above readings. Severe HTN is any BP reading > 180/110mmHg', max_length=15, null=True, verbose_name='Does the patient have severe hypertension?'),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='staying_nearby_6',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, null=True, verbose_name='Is the patient planning to remain in the catchment area for at least 6 months'),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='sys_blood_pressure',
            field=edc_vitals.models.fields.blood_pressure.SystolicPressureField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='sys_blood_pressure_avg',
            field=models.IntegerField(blank=True, null=True, verbose_name='Blood pressure: systolic (average)'),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='sys_blood_pressure_one',
            field=edc_vitals.models.fields.blood_pressure.SystolicPressureField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalsubjectscreening',
            name='sys_blood_pressure_two',
            field=edc_vitals.models.fields.blood_pressure.SystolicPressureField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='appt_datetime',
            field=models.DateTimeField(blank=True, help_text='Leave blank if continuing to the second stage today', null=True, verbose_name='Appointment date for second stage of screening (P2)'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='continue_part_two',
            field=models.CharField(choices=[('Yes', 'Yes (default)'), ('No', 'No')], default='Yes', help_text='<B>Important</B>: This response will be be automatically set to YES if:<BR><BR>- the participant meets the eligibility criteria for part one, or;<BR><BR>- the eligibility criteria for part two is already complete.<BR>', max_length=15, verbose_name='Continue with <U>part two</U> of the screening process?'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='dia_blood_pressure',
            field=edc_vitals.models.fields.blood_pressure.DiastolicPressureField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='dia_blood_pressure_avg',
            field=models.IntegerField(blank=True, null=True, verbose_name='Blood pressure: diastolic (average)'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='dia_blood_pressure_one',
            field=edc_vitals.models.fields.blood_pressure.DiastolicPressureField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='dia_blood_pressure_two',
            field=edc_vitals.models.fields.blood_pressure.DiastolicPressureField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='fasted',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, null=True, verbose_name='Did the patient come to the clinic fasted?'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='fasting',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='As reported by patient', max_length=15, null=True, verbose_name='Has the participant fasted?'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='fasting_duration_minutes',
            field=models.IntegerField(help_text='system calculated value', null=True),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='fasting_duration_str',
            field=models.CharField(blank=True, help_text='As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc', max_length=8, null=True, validators=[django.core.validators.RegexValidator('^([0-9]{1,3}h([0-5]?[0-9]m)?)$', message='Invalid format. Expected something like 1h20m, 11h5m, etc')], verbose_name='How long have they fasted in hours and/or minutes?'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='fbg_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='<u>Time</u> FBG level measured'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='fbg_quantifier',
            field=models.CharField(choices=[('=', '='), ('>', '>'), ('>=', '>='), ('<', '<'), ('<=', '<=')], default='=', max_length=10, verbose_name='FBG quantifier'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='fbg_units',
            field=models.CharField(blank=True, choices=[('mg/dL', 'mg/dL'), ('mmol/L', 'mmol/L (millimoles/L)')], max_length=15, null=True, verbose_name='FBG units'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='fbg_value',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='A `HIGH` reading may be entered as 9999.99', max_digits=8, null=True, verbose_name='FBG level'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='part_two_report_datetime',
            field=models.DateTimeField(help_text='Date and time of report.', null=True, verbose_name='Part 2 report date and time'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='patient_conditions',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, null=True, verbose_name='The participant has at least one of the following conditions: HIV, diabetes or hypertension?'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='severe_htn',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], help_text='Based on the above readings. Severe HTN is any BP reading > 180/110mmHg', max_length=15, null=True, verbose_name='Does the patient have severe hypertension?'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='staying_nearby_6',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, null=True, verbose_name='Is the patient planning to remain in the catchment area for at least 6 months'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='sys_blood_pressure',
            field=edc_vitals.models.fields.blood_pressure.SystolicPressureField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='sys_blood_pressure_avg',
            field=models.IntegerField(blank=True, null=True, verbose_name='Blood pressure: systolic (average)'),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='sys_blood_pressure_one',
            field=edc_vitals.models.fields.blood_pressure.SystolicPressureField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subjectscreening',
            name='sys_blood_pressure_two',
            field=edc_vitals.models.fields.blood_pressure.SystolicPressureField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='HistoricalScreeningPartTwo',
            fields=[
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('created', models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow)),
                ('modified', models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow)),
                ('user_created', django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', django_audit_fields.fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.')),
                ('subject_identifier', models.CharField(max_length=50)),
                ('subject_identifier_as_pk', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('subject_identifier_aka', models.CharField(editable=False, help_text='track a previously allocated identifier.', max_length=50, null=True, verbose_name='Subject Identifier a.k.a')),
                ('slug', models.CharField(db_index=True, default='', editable=False, help_text='a field used for quick search', max_length=250, null=True)),
                ('eligible', models.BooleanField(default=False, editable=False)),
                ('reasons_ineligible', models.TextField(editable=False, max_length=150, null=True, verbose_name='Reason not eligible')),
                ('eligibility_datetime', models.DateTimeField(editable=False, help_text='Date and time eligibility was determined relative to report_datetime', null=True)),
                ('real_eligibility_datetime', models.DateTimeField(editable=False, help_text='Date and time eligibility was determined relative to now', null=True)),
                ('reference', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, verbose_name='Reference')),
                ('screening_identifier', models.CharField(blank=True, db_index=True, editable=False, max_length=50, verbose_name='Screening ID')),
                ('report_datetime', models.DateTimeField(default=edc_utils.date.get_utcnow, help_text='Date and time of report.', verbose_name='Report Date and Time')),
                ('initials', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(blank=True, help_text='Use UPPERCASE letters only. May be 2 or 3 letters. (Encryption: RSA local)', max_length=71, validators=[django.core.validators.RegexValidator('[A-Z]{1,3}', 'Invalid format'), django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(3)])),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=10)),
                ('age_in_years', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(110)])),
                ('consent_ability', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=25, verbose_name='Participant or legal guardian/representative able and willing to give informed consent.')),
                ('unsuitable_for_study', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', help_text='If YES, patient NOT eligible, please give reason below.', max_length=5, verbose_name='Is there any other reason the patient is deemed to not be suitable for the study?')),
                ('reasons_unsuitable', models.TextField(blank=True, max_length=150, null=True, verbose_name='Reason not suitable for the study')),
                ('unsuitable_agreed', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', max_length=5, verbose_name='Does the study coordinator agree that the patient is not suitable for the study?')),
                ('consented', models.BooleanField(default=False, editable=False)),
                ('refused', models.BooleanField(default=False, editable=False)),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('screening_consent', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, verbose_name='Has the subject given his/her verbal consent to be screened for the INTECOMM trial?')),
                ('patient_conditions', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, null=True, verbose_name='The participant has at least one of the following conditions: HIV, diabetes or hypertension?')),
                ('staying_nearby_6', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, null=True, verbose_name='Is the patient planning to remain in the catchment area for at least 6 months')),
                ('fasted', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, null=True, verbose_name='Did the patient come to the clinic fasted?')),
                ('appt_datetime', models.DateTimeField(blank=True, help_text='Leave blank if continuing to the second stage today', null=True, verbose_name='Appointment date for second stage of screening (P2)')),
                ('continue_part_two', models.CharField(choices=[('Yes', 'Yes (default)'), ('No', 'No')], default='Yes', help_text='<B>Important</B>: This response will be be automatically set to YES if:<BR><BR>- the participant meets the eligibility criteria for part one, or;<BR><BR>- the eligibility criteria for part two is already complete.<BR>', max_length=15, verbose_name='Continue with <U>part two</U> of the screening process?')),
                ('sys_blood_pressure', edc_vitals.models.fields.blood_pressure.SystolicPressureField(blank=True, null=True)),
                ('dia_blood_pressure', edc_vitals.models.fields.blood_pressure.DiastolicPressureField(blank=True, null=True)),
                ('sys_blood_pressure_one', edc_vitals.models.fields.blood_pressure.SystolicPressureField(blank=True, null=True)),
                ('dia_blood_pressure_one', edc_vitals.models.fields.blood_pressure.DiastolicPressureField(blank=True, null=True)),
                ('sys_blood_pressure_two', edc_vitals.models.fields.blood_pressure.SystolicPressureField(blank=True, null=True)),
                ('dia_blood_pressure_two', edc_vitals.models.fields.blood_pressure.DiastolicPressureField(blank=True, null=True)),
                ('sys_blood_pressure_avg', models.IntegerField(blank=True, null=True, verbose_name='Blood pressure: systolic (average)')),
                ('dia_blood_pressure_avg', models.IntegerField(blank=True, null=True, verbose_name='Blood pressure: diastolic (average)')),
                ('severe_htn', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], help_text='Based on the above readings. Severe HTN is any BP reading > 180/110mmHg', max_length=15, null=True, verbose_name='Does the patient have severe hypertension?')),
                ('fasting', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='As reported by patient', max_length=15, null=True, verbose_name='Has the participant fasted?')),
                ('fasting_duration_str', models.CharField(blank=True, help_text='As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc', max_length=8, null=True, validators=[django.core.validators.RegexValidator('^([0-9]{1,3}h([0-5]?[0-9]m)?)$', message='Invalid format. Expected something like 1h20m, 11h5m, etc')], verbose_name='How long have they fasted in hours and/or minutes?')),
                ('fasting_duration_minutes', models.IntegerField(help_text='system calculated value', null=True)),
                ('fbg_units', models.CharField(blank=True, choices=[('mg/dL', 'mg/dL'), ('mmol/L', 'mmol/L (millimoles/L)')], max_length=15, null=True, verbose_name='FBG units')),
                ('fbg_value', models.DecimalField(blank=True, decimal_places=2, help_text='A `HIGH` reading may be entered as 9999.99', max_digits=8, null=True, verbose_name='FBG level')),
                ('fbg_quantifier', models.CharField(choices=[('=', '='), ('>', '>'), ('>=', '>='), ('<', '<'), ('<=', '<=')], default='=', max_length=10, verbose_name='FBG quantifier')),
                ('fbg_datetime', models.DateTimeField(blank=True, null=True, verbose_name='<u>Time</u> FBG level measured')),
                ('part_two_report_datetime', models.DateTimeField(help_text='Date and time of report.', null=True, verbose_name='Part 2 report date and time')),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(blank=True, db_constraint=False, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sites.site')),
            ],
            options={
                'verbose_name': 'historical Subject Screening: Part Two',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalScreeningPartOne',
            fields=[
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('created', models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow)),
                ('modified', models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow)),
                ('user_created', django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', django_audit_fields.fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.')),
                ('subject_identifier', models.CharField(max_length=50)),
                ('subject_identifier_as_pk', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('subject_identifier_aka', models.CharField(editable=False, help_text='track a previously allocated identifier.', max_length=50, null=True, verbose_name='Subject Identifier a.k.a')),
                ('slug', models.CharField(db_index=True, default='', editable=False, help_text='a field used for quick search', max_length=250, null=True)),
                ('eligible', models.BooleanField(default=False, editable=False)),
                ('reasons_ineligible', models.TextField(editable=False, max_length=150, null=True, verbose_name='Reason not eligible')),
                ('eligibility_datetime', models.DateTimeField(editable=False, help_text='Date and time eligibility was determined relative to report_datetime', null=True)),
                ('real_eligibility_datetime', models.DateTimeField(editable=False, help_text='Date and time eligibility was determined relative to now', null=True)),
                ('reference', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, verbose_name='Reference')),
                ('screening_identifier', models.CharField(blank=True, db_index=True, editable=False, max_length=50, verbose_name='Screening ID')),
                ('report_datetime', models.DateTimeField(default=edc_utils.date.get_utcnow, help_text='Date and time of report.', verbose_name='Report Date and Time')),
                ('initials', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(blank=True, help_text='Use UPPERCASE letters only. May be 2 or 3 letters. (Encryption: RSA local)', max_length=71, validators=[django.core.validators.RegexValidator('[A-Z]{1,3}', 'Invalid format'), django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(3)])),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=10)),
                ('age_in_years', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(110)])),
                ('consent_ability', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=25, verbose_name='Participant or legal guardian/representative able and willing to give informed consent.')),
                ('unsuitable_for_study', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', help_text='If YES, patient NOT eligible, please give reason below.', max_length=5, verbose_name='Is there any other reason the patient is deemed to not be suitable for the study?')),
                ('reasons_unsuitable', models.TextField(blank=True, max_length=150, null=True, verbose_name='Reason not suitable for the study')),
                ('unsuitable_agreed', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', max_length=5, verbose_name='Does the study coordinator agree that the patient is not suitable for the study?')),
                ('consented', models.BooleanField(default=False, editable=False)),
                ('refused', models.BooleanField(default=False, editable=False)),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('screening_consent', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, verbose_name='Has the subject given his/her verbal consent to be screened for the INTECOMM trial?')),
                ('patient_conditions', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, null=True, verbose_name='The participant has at least one of the following conditions: HIV, diabetes or hypertension?')),
                ('staying_nearby_6', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, null=True, verbose_name='Is the patient planning to remain in the catchment area for at least 6 months')),
                ('fasted', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=15, null=True, verbose_name='Did the patient come to the clinic fasted?')),
                ('appt_datetime', models.DateTimeField(blank=True, help_text='Leave blank if continuing to the second stage today', null=True, verbose_name='Appointment date for second stage of screening (P2)')),
                ('continue_part_two', models.CharField(choices=[('Yes', 'Yes (default)'), ('No', 'No')], default='Yes', help_text='<B>Important</B>: This response will be be automatically set to YES if:<BR><BR>- the participant meets the eligibility criteria for part one, or;<BR><BR>- the eligibility criteria for part two is already complete.<BR>', max_length=15, verbose_name='Continue with <U>part two</U> of the screening process?')),
                ('sys_blood_pressure', edc_vitals.models.fields.blood_pressure.SystolicPressureField(blank=True, null=True)),
                ('dia_blood_pressure', edc_vitals.models.fields.blood_pressure.DiastolicPressureField(blank=True, null=True)),
                ('sys_blood_pressure_one', edc_vitals.models.fields.blood_pressure.SystolicPressureField(blank=True, null=True)),
                ('dia_blood_pressure_one', edc_vitals.models.fields.blood_pressure.DiastolicPressureField(blank=True, null=True)),
                ('sys_blood_pressure_two', edc_vitals.models.fields.blood_pressure.SystolicPressureField(blank=True, null=True)),
                ('dia_blood_pressure_two', edc_vitals.models.fields.blood_pressure.DiastolicPressureField(blank=True, null=True)),
                ('sys_blood_pressure_avg', models.IntegerField(blank=True, null=True, verbose_name='Blood pressure: systolic (average)')),
                ('dia_blood_pressure_avg', models.IntegerField(blank=True, null=True, verbose_name='Blood pressure: diastolic (average)')),
                ('severe_htn', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], help_text='Based on the above readings. Severe HTN is any BP reading > 180/110mmHg', max_length=15, null=True, verbose_name='Does the patient have severe hypertension?')),
                ('fasting', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='As reported by patient', max_length=15, null=True, verbose_name='Has the participant fasted?')),
                ('fasting_duration_str', models.CharField(blank=True, help_text='As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc', max_length=8, null=True, validators=[django.core.validators.RegexValidator('^([0-9]{1,3}h([0-5]?[0-9]m)?)$', message='Invalid format. Expected something like 1h20m, 11h5m, etc')], verbose_name='How long have they fasted in hours and/or minutes?')),
                ('fasting_duration_minutes', models.IntegerField(help_text='system calculated value', null=True)),
                ('fbg_units', models.CharField(blank=True, choices=[('mg/dL', 'mg/dL'), ('mmol/L', 'mmol/L (millimoles/L)')], max_length=15, null=True, verbose_name='FBG units')),
                ('fbg_value', models.DecimalField(blank=True, decimal_places=2, help_text='A `HIGH` reading may be entered as 9999.99', max_digits=8, null=True, verbose_name='FBG level')),
                ('fbg_quantifier', models.CharField(choices=[('=', '='), ('>', '>'), ('>=', '>='), ('<', '<'), ('<=', '<=')], default='=', max_length=10, verbose_name='FBG quantifier')),
                ('fbg_datetime', models.DateTimeField(blank=True, null=True, verbose_name='<u>Time</u> FBG level measured')),
                ('part_two_report_datetime', models.DateTimeField(help_text='Date and time of report.', null=True, verbose_name='Part 2 report date and time')),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(blank=True, db_constraint=False, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sites.site')),
            ],
            options={
                'verbose_name': 'historical Subject Screening: Part One',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]