from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.sites.models import Site
from edc_appointment.constants import IN_PROGRESS_APPT, INCOMPLETE_APPT
from edc_appointment.tests.test_case_mixins import AppointmentTestCaseMixin
from edc_constants.constants import DM, FEMALE, HIV, HTN, NO, NOT_APPLICABLE, YES
from edc_facility.import_holidays import import_holidays
from edc_list_data.site_list_data import site_list_data
from edc_metadata import REQUIRED
from edc_metadata.models import CrfMetadata
from edc_randomization.site_randomizers import site_randomizers
from edc_sites import add_or_update_django_sites, get_sites_by_country
from edc_visit_schedule.constants import DAY1
from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_bakery import baker
from model_bakery.baker import make_recipe

from intecomm_lists.models import Conditions
from intecomm_sites.sites import fqdn
from intecomm_sites.tests.site_test_case_mixin import SiteTestCaseMixin
from intecomm_subject.models import SubjectVisit

from ..models import ConsentRefusal, PatientLog, SubjectScreening

fake = Faker()
now = datetime(2019, 5, 1).astimezone(ZoneInfo("UTC"))
tomorrow = now + relativedelta(days=1)


def get_eligible_options(patient_log: PatientLog):
    hiv_dx = True if patient_log.conditions.filter(name=HIV) else False
    dm_dx = True if patient_log.conditions.filter(name=DM) else False
    htn_dx = True if patient_log.conditions.filter(name=HTN) else False
    return dict(
        report_datetime=now,
        patient_log=patient_log,
        legal_name=patient_log.legal_name,
        familiar_name=patient_log.familiar_name,
        initials=patient_log.initials,
        hospital_identifier=patient_log.hospital_identifier,
        gender=patient_log.gender,
        age_in_years=patient_log.age_in_years,
        in_care_6m=YES,
        lives_nearby=YES,
        staying_nearby_6=YES,
        pregnant=NOT_APPLICABLE,
        excluded_by_bp_history=NO,
        excluded_by_gluc_history=NO,
        requires_acute_care=NO,
        hiv_dx=YES if hiv_dx else NO,
        hiv_dx_6m=YES if hiv_dx else NOT_APPLICABLE,
        hiv_dx_ago="1y" if hiv_dx else None,
        art_unchanged_3m=YES if hiv_dx else NOT_APPLICABLE,
        art_stable=YES if hiv_dx else NOT_APPLICABLE,
        art_adherent=YES if hiv_dx else NOT_APPLICABLE,
        dm_dx=YES if dm_dx else NO,
        dm_dx_6m=YES if dm_dx else NO,
        dm_dx_ago="1y" if dm_dx else None,
        dm_complications=NO if dm_dx else NOT_APPLICABLE,
        htn_dx=YES if htn_dx else NO,
        htn_dx_6m=YES if htn_dx else NO,
        htn_dx_ago="1y" if htn_dx else None,
        htn_complications=NO if htn_dx else NOT_APPLICABLE,
        sys_blood_pressure_one=120,
        dia_blood_pressure_one=80,
        sys_blood_pressure_two=120,
        dia_blood_pressure_two=80,
        consent_ability=YES,
        unsuitable_for_study=NO,
        unsuitable_agreed=NOT_APPLICABLE,
    )


class IntecommTestCaseMixin(AppointmentTestCaseMixin, SiteTestCaseMixin):
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

    @staticmethod
    def get_patient_log(
        legal_name: str | None = None,
        familiar_name: str | None = None,
        initials: str | None = None,
        gender: str | None = None,
        age_in_years: int | None = None,
        hospital_identifier: str | None = None,
        conditions: list[Conditions] | None = None,
        **kwargs,
    ):
        opts = dict(
            legal_name=legal_name or "NAMEA AAA",
            familiar_name=familiar_name or "NAMEA",
            initials=initials or "NA",
            gender=gender or FEMALE,
            age_in_years=age_in_years or 20,
            hospital_identifier=hospital_identifier or uuid4().hex,
            contact_number="1234567890",
        )
        opts.update(**kwargs)
        patient_log = make_recipe("intecomm_screening.patientlog", **opts)
        conditions = conditions or [HIV]
        for condition in conditions:
            patient_log.conditions.add(Conditions.objects.get(name=condition))
        return patient_log

    def get_subject_screening(
        self,
        patient_log: PatientLog | None = None,
        report_datetime: datetime | None = None,
        eligibility_datetime: datetime | None = None,
        gender: str | None = None,
        age_in_years: int | None = None,
        conditions: list[Conditions] | None = None,
        patient_log_options: dict | None = None,
    ):
        patient_log_opt = dict(
            gender=gender,
            age_in_years=age_in_years,
            conditions=conditions,
        )
        patient_log_opt.update(**(patient_log_options or {}))
        patient_log = patient_log or self.get_patient_log(**patient_log_opt)
        eligible_options = deepcopy(get_eligible_options(patient_log=patient_log))
        eligible_options.update(report_datetime=report_datetime or now)
        subject_screening = SubjectScreening.objects.create(
            patient_log_identifier=patient_log.patient_log_identifier,
            user_created="erikvw",
            user_modified="erikvw",
            **eligible_options,
        )
        screening_identifier = subject_screening.screening_identifier
        self.assertEqual(subject_screening.reasons_ineligible, None)
        self.assertTrue(subject_screening.eligible)

        subject_screening = SubjectScreening.objects.get(
            screening_identifier=screening_identifier
        )
        self.assertTrue(subject_screening.eligible)

        patient_log.screening_identifier = screening_identifier
        patient_log.save()

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
            legal_name=subject_screening.legal_name,
            familiar_name=subject_screening.familiar_name,
            initials=subject_screening.initials,
            gender=subject_screening.gender,
            dob=(now.date() - relativedelta(years=subject_screening.age_in_years)),
            identity=subject_screening.hospital_identifier,
            confirm_identity=subject_screening.hospital_identifier,
            site=Site.objects.get(id=site_id or settings.SITE_ID),
            consent_datetime=consent_datetime or subject_screening.report_datetime,
            version=1,
        )

    def get_subject_visit(
        self,
        visit_code: str | None = None,
        visit_code_sequence: int | None = None,
        subject_screening=None,
        subject_consent=None,
        reason: str | None = None,
        appt_datetime: datetime | None = None,
        gender: str | None = None,
        ethnicity: str | None = None,
        age_in_years: int | None = None,
        screening_datetime: datetime | None = None,
        eligibility_datetime: datetime | None = None,
    ):
        reason = reason or SCHEDULED
        subject_screening = subject_screening or self.get_subject_screening(
            gender=gender,
            age_in_years=age_in_years,
            report_datetime=screening_datetime,
            eligibility_datetime=eligibility_datetime,
        )
        subject_consent = subject_consent or self.get_subject_consent(subject_screening)
        options = dict(
            subject_identifier=subject_consent.subject_identifier,
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

    @staticmethod
    def get_consent_refusal(screening_identifier: str):
        return ConsentRefusal.objects.create(
            user_created="jw",
            user_modified="jw",
            screening_identifier=screening_identifier,
        )
