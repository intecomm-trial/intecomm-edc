from __future__ import annotations

import secrets
import string
from datetime import datetime
from zoneinfo import ZoneInfo

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import QuerySet
from django.test import TestCase
from edc_appointment.constants import IN_PROGRESS_APPT, INCOMPLETE_APPT
from edc_appointment.tests.appointment_test_case_mixin import AppointmentTestCaseMixin
from edc_constants.constants import (
    COMPLETE,
    DM,
    FEMALE,
    HIV,
    HTN,
    MALE,
    NO,
    NOT_APPLICABLE,
    YES,
)
from edc_facility.import_holidays import import_holidays
from edc_list_data.site_list_data import site_list_data
from edc_metadata import REQUIRED
from edc_metadata.models import CrfMetadata
from edc_randomization.site_randomizers import site_randomizers
from edc_sites import add_or_update_django_sites, get_sites_by_country
from edc_utils import get_utcnow
from edc_visit_schedule.constants import DAY1
from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_bakery import baker

from intecomm_group.models import PatientGroup
from intecomm_lists.models import Conditions
from intecomm_screening.models import PatientLog, SubjectScreening
from intecomm_sites.sites import fqdn
from intecomm_sites.tests.site_test_case_mixin import SiteTestCaseMixin
from intecomm_subject.models import SubjectVisit

fake = Faker()
now = datetime(2019, 5, 1).astimezone(ZoneInfo("UTC"))
tomorrow = now + relativedelta(days=1)


class TestCaseMixin(AppointmentTestCaseMixin, SiteTestCaseMixin, TestCase):
    fqdn = fqdn

    default_sites = get_sites_by_country("tanzania")

    site_names = [s.name for s in default_sites]

    import_randomization_list = True

    sid_count_for_tests = 5

    @classmethod
    def setUpTestData(cls):
        import_holidays(test=True)
        add_or_update_django_sites(sites=get_sites_by_country("tanzania"))
        if cls.import_randomization_list:
            randomizer_cls = site_randomizers.get("default")
            randomizer_cls.import_list(
                verbose=False, sid_count_for_tests=cls.sid_count_for_tests
            )
        site_list_data.initialize()
        site_list_data.autodiscover()

    def get_subject_screening(
        self,
        patient_log: PatientLog | None = None,
        report_datetime: datetime | None = None,
        eligibility_datetime: datetime | None = None,
        gender: str | None = None,
        age_in_years: int | None = None,
        **kwargs,
    ):
        subject_screening = SubjectScreening.objects.create(
            patient_log=patient_log,
            user_created="erikvw",
            user_modified="erikvw",
            age_in_years=age_in_years,
            gender=gender,
            report_datetime=report_datetime,
            **kwargs,
        )
        screening_identifier = subject_screening.screening_identifier
        self.assertEqual(subject_screening.reasons_ineligible, None)
        self.assertEqual(subject_screening.eligible, True)

        subject_screening = SubjectScreening.objects.get(
            screening_identifier=screening_identifier
        )

        self.assertTrue(subject_screening.eligible)

        if eligibility_datetime:
            subject_screening.eligibility_datetime = eligibility_datetime
            subject_screening.save()
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=screening_identifier
            )
        return subject_screening

    @staticmethod
    def get_subject_consent(subject_screening, consent_datetime=None, site_id=None):
        return baker.make_recipe(
            "intecomm_consent.subjectconsent",
            user_created="erikvw",
            user_modified="erikvw",
            screening_identifier=subject_screening.screening_identifier,
            initials=subject_screening.initials,
            gender=subject_screening.gender,
            dob=(now.date() - relativedelta(years=subject_screening.age_in_years)),
            site=Site.objects.get(id=site_id or settings.SITE_ID),
            consent_datetime=consent_datetime or subject_screening.report_datetime,
            legal_name=subject_screening.patient_log.legal_name,
            familiar_name=subject_screening.patient_log.familiar_name,
        )

    def get_subject_visit(
        self,
        subject_identifier=None,
        visit_code: str | None = None,
        visit_code_sequence: int | None = None,
        reason: str | None = None,
        appt_datetime: datetime | None = None,
    ):
        reason = reason or SCHEDULED
        options = dict(
            subject_identifier=subject_identifier,
            visit_code=visit_code or DAY1,
            visit_code_sequence=(
                visit_code_sequence if visit_code_sequence is not None else 0
            ),
            reason=reason,
        )
        if appt_datetime:
            options.update(appt_datetime=appt_datetime)
        appointment = self.get_appointment(**options)
        subject_visit = SubjectVisit(
            appointment=appointment,
            reason=SCHEDULED,
            report_datetime=appointment.appt_datetime,
        )
        subject_visit.save()
        subject_visit.refresh_from_db()
        return subject_visit

    @staticmethod
    def get_next_subject_visit(subject_visit):
        appointment = subject_visit.appointment
        appointment.appt_status = INCOMPLETE_APPT
        appointment.save()
        appointment.refresh_from_db()
        next_appointment = appointment.next_by_timepoint
        next_appointment.appt_status = IN_PROGRESS_APPT
        next_appointment.save()
        subject_visit = SubjectVisit(
            appointment=next_appointment,
            reason=SCHEDULED,
            report_datetime=next_appointment.appt_datetime,
            visit_code=next_appointment.visit_code,
            visit_code_sequence=next_appointment.visit_code_sequence,
        )
        subject_visit.save()
        subject_visit.refresh_from_db()
        return subject_visit

    @staticmethod
    def get_crf_metadata(subject_visit):
        return CrfMetadata.objects.filter(
            subject_identifier=subject_visit.subject_identifier,
            visit_code=subject_visit.visit_code,
            visit_code_sequence=subject_visit.visit_code_sequence,
            entry_status=REQUIRED,
        )

    def get_patients(
        self,
        dm: int = None,
        htn: int = None,
        hiv: int = None,
        ncd: int = None,
        hiv_ncd: int = None,
        stable: bool | None = None,
        screen: bool | None = None,
        consent: bool | None = None,
    ) -> list[PatientLog]:
        """Returns a list of patient log model instances"""
        patients = []
        default_ratio = (5, 5, 4, 0, 0)
        ratio = (dm or 0, htn or 0, hiv or 0, ncd or 0, hiv_ncd or 0) or default_ratio
        for i in range(0, ratio[0]):
            patients.append(self.get_patient_log([DM], i + 100, stable, screen, consent))
        for i in range(0, ratio[1]):
            patients.append(self.get_patient_log([HTN], i + 200, stable, screen, consent))
        for i in range(0, ratio[2]):
            patients.append(self.get_patient_log([HIV], i + 300, stable, screen, consent))
        for i in range(0, ratio[3]):
            patients.append(self.get_patient_log([DM, HTN], i + 300, stable, screen, consent))
        for i in range(0, ratio[4]):
            patients.append(
                self.get_patient_log([HIV, DM, HTN], i + 300, stable, screen, consent)
            )
        return patients

    def get_patient_log(
        self,
        conditions: list[str],
        i: int | None = None,
        stable: bool | None = None,
        screen: bool | None = None,
        consent: bool | None = None,
        report_datetime=None,
        gender: str | None = None,
    ) -> PatientLog:
        """Returns a patient log model instance"""
        report_datetime = report_datetime or get_utcnow() - relativedelta(days=15)
        stable = YES if stable else NO
        first_name = fake.first_name()
        last_name = fake.last_name()
        contact_number = ""
        for i in range(10):
            contact_number += "".join(secrets.choice(string.digits))
        initials = ""
        for i in range(2):
            initials += "".join(secrets.choice(string.ascii_uppercase + string.digits))
        patient_log = PatientLog.objects.create(
            report_datetime=report_datetime,
            gender=gender or FEMALE,
            legal_name=f"{first_name} {last_name}",
            familiar_name=f"{first_name}",
            initials=initials,
            hospital_identifier=secrets.token_urlsafe(),
            contact_number=contact_number,
            stable=stable,
            last_appt_date=None,
            age_in_years=25,
            site=Site.objects.get(id=settings.SITE_ID),
            next_appt_date=report_datetime + relativedelta(days=45),
        )
        for condition in Conditions.objects.filter(name__in=[x for x in conditions]):
            patient_log.conditions.add(condition)
        if screen:
            hiv_dx = YES if HIV in [obj.name for obj in patient_log.conditions.all()] else NO
            dm_dx = YES if DM in [obj.name for obj in patient_log.conditions.all()] else NO
            htn_dx = YES if HTN in [obj.name for obj in patient_log.conditions.all()] else NO
            screening_options = dict(
                report_datetime=report_datetime + relativedelta(days=1),
                gender=patient_log.gender,
                legal_name=patient_log.legal_name,
                familiar_name=patient_log.legal_name,
                initials=patient_log.initials,
                consent_ability=YES,
                age_in_years=patient_log.age_in_years,
                patient_log=patient_log,
                hospital_identifier=patient_log.hospital_identifier,
                lives_nearby=YES,
                staying_nearby_6=YES,
                in_care_6m=YES,
                in_care_duration="2y",
                hiv_dx=hiv_dx,
                hiv_dx_6m=NOT_APPLICABLE if hiv_dx == NO else YES,
                hiv_dx_ago=None if hiv_dx == NO else "2y",
                art_stable=NOT_APPLICABLE if hiv_dx == NO else YES,
                art_adherent=NOT_APPLICABLE if hiv_dx == NO else YES,
                dm_dx=dm_dx,
                dm_dx_6m=NOT_APPLICABLE if dm_dx == NO else YES,
                dm_dx_ago=None if dm_dx == NO else "2y",
                dm_complications=NOT_APPLICABLE if dm_dx == NO else NO,
                htn_dx=htn_dx,
                htn_dx_6m=NOT_APPLICABLE if htn_dx == NO else YES,
                htn_dx_ago=None if htn_dx == NO else "2y",
                htn_complications=NOT_APPLICABLE if htn_dx == NO else NO,
                excluded_by_bp_history=NO,
                excluded_by_gluc_history=NO,
                requires_acute_care=NO,
                pregnant=NOT_APPLICABLE if patient_log.gender == MALE else NO,
                sys_blood_pressure_one=120,
                sys_blood_pressure_two=120,
                dia_blood_pressure_one=80,
                dia_blood_pressure_two=80,
            )
            subject_screening = self.get_subject_screening(**screening_options)
            if consent:
                self.get_subject_consent(
                    subject_screening, consent_datetime=report_datetime + relativedelta(days=2)
                )
        patient_log.refresh_from_db()
        return patient_log

    @staticmethod
    def get_patient_group(patient_logs: QuerySet, name: str = None) -> PatientGroup:
        patient_group = PatientGroup.objects.create(name=name or "GROUP1")
        for patient in patient_logs.filter(conditions__name__in=[HIV]).exclude(
            conditions__name__in=[HTN, DM]
        ):
            patient_group.hiv_patients.add(patient)
        for patient in patient_logs.filter(conditions__name__in=[DM]).exclude(
            conditions__name__in=[HTN, HIV]
        ):
            patient_group.dm_patients.add(patient)

        for patient in patient_logs.filter(conditions__name__in=[HTN]).exclude(
            conditions__name__in=[DM, HIV]
        ):
            patient_group.htn_patients.add(patient)
        return patient_group

    @staticmethod
    def randomize_patient_group(
        patient_group: PatientGroup,
        status: str | None = None,
        randomize_now: str | None = None,
        confirm_randomize_now: str | None = None,
    ) -> PatientGroup:
        patient_group.status = status or COMPLETE
        patient_group.save()
        patient_group.randomize_now = randomize_now or YES
        patient_group.confirm_randomize_now = confirm_randomize_now or "RANDOMIZE"
        patient_group.save()
        patient_group.refresh_from_db()
        return patient_group
