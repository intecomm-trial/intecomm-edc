from __future__ import annotations

import random
import string
from copy import deepcopy
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4
from zoneinfo import ZoneInfo

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from edc_appointment.constants import IN_PROGRESS_APPT, INCOMPLETE_APPT
from edc_appointment.models import Appointment
from edc_appointment.tests.test_case_mixins import AppointmentTestCaseMixin
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
from edc_metadata.models import CrfMetadata
from edc_randomization.site_randomizers import site_randomizers
from edc_sites.site import sites
from edc_sites.utils import add_or_update_django_sites
from edc_utils import get_utcnow
from edc_visit_schedule.constants import DAY1
from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from intecomm_rando.constants import UGANDA
from model_bakery import baker
from model_bakery.baker import make_recipe
from tqdm import tqdm

from intecomm_lists.models import Conditions
from intecomm_screening.models import (
    ConsentRefusal,
    PatientGroup,
    PatientGroupRando,
    PatientLog,
    SubjectScreeningTz,
    SubjectScreeningUg,
)
from intecomm_sites.sites import fqdn
from intecomm_sites.tests.site_test_case_mixin import SiteTestCaseMixin
from intecomm_subject.models import ClinicalReview, ClinicalReviewBaseline, SubjectVisit

if TYPE_CHECKING:
    from intecomm_consent.models import SubjectConsent, SubjectConsentUg

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


def get_current_country(site_id):
    if site_id <= 200:
        return UGANDA
    return "tanzania"


class IntecommTestCaseMixin(AppointmentTestCaseMixin, SiteTestCaseMixin):
    fqdn = fqdn

    default_sites = sites.get_by_country("tanzania", aslist=True)

    site_names = [s.name for s in default_sites]

    import_randomization_list = True

    sid_count_for_tests = 5

    @classmethod
    def setUpTestData(cls):
        import_holidays(test=True)
        sites.autodiscover()
        add_or_update_django_sites()
        if cls.import_randomization_list:
            randomizer_cls = site_randomizers.get("default")
            randomizer_cls.import_list(
                verbose=False, sid_count_for_tests=cls.sid_count_for_tests
            )
        site_list_data.initialize()
        site_list_data.autodiscover()

    @classmethod
    def get_patient_log(
        cls,
        legal_name: str | None = None,
        familiar_name: str | None = None,
        initials: str | None = None,
        gender: str | None = None,
        age_in_years: int | None = None,
        hospital_identifier: str | None = None,
        conditions: list[Conditions] | None = None,
        country: str | None = None,
        site: int | None = None,
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
            site=site or Site.objects.get(id=settings.SITE_ID),
        )
        opts.update(**kwargs)
        if country == UGANDA:
            patient_log = make_recipe("intecomm_screening.patientlogug", **opts)
        else:
            patient_log = make_recipe("intecomm_screening.patientlog", **opts)
        conditions = conditions or [HIV]
        for condition in conditions:
            patient_log.conditions.add(Conditions.objects.get(name=condition))
        return patient_log

    @classmethod
    def get_subject_screening(
        cls,
        patient_log: PatientLog | None = None,
        report_datetime: datetime | None = None,
        eligibility_datetime: datetime | None = None,
        gender: str | None = None,
        age_in_years: int | None = None,
        conditions: list[Conditions] | None = None,
        patient_log_options: dict | None = None,
    ) -> [SubjectScreeningTz, SubjectScreeningUg]:
        patient_log_opt = dict(
            gender=gender,
            age_in_years=age_in_years,
            conditions=conditions,
        )
        patient_log_opt.update(**(patient_log_options or {}))
        country = get_current_country(settings.SITE_ID)
        patient_log = patient_log or cls.get_patient_log(country=country, **patient_log_opt)
        eligible_options = deepcopy(get_eligible_options(patient_log=patient_log))
        eligible_options.update(report_datetime=report_datetime or now)
        if country == UGANDA:
            subject_screening_model_cls = SubjectScreeningUg
        else:
            subject_screening_model_cls = SubjectScreeningTz
        subject_screening = subject_screening_model_cls.objects.create(
            patient_log_identifier=patient_log.patient_log_identifier,
            user_created="erikvw",
            user_modified="erikvw",
            **eligible_options,
        )
        screening_identifier = subject_screening.screening_identifier

        subject_screening = subject_screening_model_cls.objects.get(
            screening_identifier=screening_identifier
        )
        patient_log.screening_identifier = screening_identifier
        patient_log.save()

        if eligibility_datetime:
            subject_screening.eligibility_datetime = eligibility_datetime
            subject_screening.save()
            subject_screening = subject_screening_model_cls.objects.get(
                screening_identifier=screening_identifier
            )
        return subject_screening

    @staticmethod
    def get_subject_consent(
        subject_screening, consent_datetime=None, site_id=None
    ) -> SubjectConsent | SubjectConsentUg:
        country = get_current_country(subject_screening.site.id)
        if country == UGANDA:
            model_name = "intecomm_consent.subjectconsentug"
        else:
            model_name = "intecomm_consent.subjectconsenttz"

        return baker.make_recipe(
            model_name,
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

    @staticmethod
    def get_crf_metadata(
        subject_visit, model: str | None = None, entry_status: str | None = None
    ):
        opts = dict(
            subject_identifier=subject_visit.subject_identifier,
            visit_code=subject_visit.visit_code,
            visit_code_sequence=subject_visit.visit_code_sequence,
        )
        if model:
            opts.update(model=model)
        if entry_status:
            opts.update(entry_status=entry_status)
        return CrfMetadata.objects.filter(**opts)

    @staticmethod
    def get_consent_refusal(screening_identifier: str):
        return ConsentRefusal.objects.create(
            user_created="jw",
            user_modified="jw",
            screening_identifier=screening_identifier,
        )

    @classmethod
    def get_consented_patient(
        cls,
        condition_name: str,
        report_datetime: datetime | None = None,
        index: int | None = None,
    ) -> SubjectConsent | SubjectConsentUg:
        """Creates patientlog->subjectscreening->subjectconsent."""
        letter = random.choice(string.ascii_lowercase)  # nosec B311
        first_name = fake.first_name()
        last_name = fake.last_name()
        legal_name = f"{first_name} {last_name}"
        initials = f"{first_name[0]}{letter}{last_name[0]}"
        report_datetime = report_datetime or get_utcnow()
        gender = random.choice([FEMALE, MALE])  # nosec B311
        age_in_years = random.choice(  # nosec B311
            [20, 25, 30, 35, 40, 45, 50, 55, 60, 65]  # nosec B311
        )
        contact_number = f"12345678{index}" if index else fake.credit_card_number()
        patient_log_options = dict(
            report_datetime=report_datetime,
            legal_name=legal_name,
            familiar_name=legal_name,
            initials=initials,
            gender=gender,
            age_in_years=age_in_years,
            hospital_identifier=uuid4().hex,
            contact_number=contact_number,
            conditions=[condition_name],
        )
        subject_screening = cls.get_subject_screening(
            patient_log_options=patient_log_options, report_datetime=report_datetime
        )
        return cls.get_subject_consent(subject_screening, consent_datetime=report_datetime)

    @classmethod
    def get_patient_group(
        cls,
        report_datetime: datetime | None = None,
        conditions: list[str] | None = None,
        group_name: str | None = None,
    ):
        conditions = conditions or ([HIV] * 4) + ([HTN] * 5) + ([DM] * 5)
        for i, condition_name in tqdm(enumerate(conditions), total=len(conditions)):
            cls.get_consented_patient(
                condition_name=condition_name, report_datetime=report_datetime, index=i
            )
        patient_group = PatientGroup.objects.create(
            name=group_name or "BRANDX", report_datetime=report_datetime
        )
        total = PatientLog.objects.filter(conditions__name__in=[HIV]).count()
        for obj in tqdm(PatientLog.objects.filter(conditions__name__in=[HIV]), total=total):
            patient_group.hiv_patients.add(obj)
        total = PatientLog.objects.filter(conditions__name__in=[HTN]).count()
        for obj in tqdm(PatientLog.objects.filter(conditions__name__in=[HTN]), total=total):
            patient_group.htn_patients.add(obj)
        total = PatientLog.objects.filter(conditions__name__in=[DM]).count()
        for obj in tqdm(PatientLog.objects.filter(conditions__name__in=[DM]), total=total):
            patient_group.dm_patients.add(obj)
        return patient_group

    @classmethod
    def get_randomized_patient_group(
        cls,
        report_datetime: datetime | None = None,
        patient_group: PatientGroup | None = None,
        conditions: list[str] | None = None,
        group_name: str | None = None,
    ):
        patient_group = patient_group or cls.get_patient_group(
            report_datetime=report_datetime,
            conditions=conditions,
            group_name=group_name,
        )
        patient_group.status = COMPLETE
        patient_group.save()

        patient_group = PatientGroupRando.objects.get(id=patient_group.id)
        patient_group.randomize_now = YES
        patient_group.confirm_randomize_now = "RANDOMIZE"
        patient_group.save()
        patient_group.refresh_from_db()
        return patient_group

    @classmethod
    def get_subject_visit(
        cls,
        visit_code: str | None = None,
        subject_identifier: str | None = None,
        report_datetime: datetime | None = None,
    ) -> SubjectVisit:
        visit_code = visit_code or DAY1
        if subject_identifier:
            appointment = Appointment.objects.get(
                visit_code=visit_code, subject_identifier=subject_identifier
            )
        else:
            appointment = Appointment.objects.filter(visit_code=visit_code)[0]
        subject_visit = SubjectVisit.objects.create(
            appointment=appointment,
            report_datetime=report_datetime or appointment.appt_datetime,
            reason=SCHEDULED,
        )
        return subject_visit

    @classmethod
    def get_next_subject_visit(
        cls,
        subject_visit,
        report_datetime: datetime | None = None,
    ):
        appointment = subject_visit.appointment
        appointment.appt_status = INCOMPLETE_APPT
        appointment.save()
        appointment.refresh_from_db()
        next_appointment = appointment.next_by_timepoint
        next_appointment.appt_status = IN_PROGRESS_APPT
        next_appointment.save()
        next_subject_visit = SubjectVisit(
            appointment=next_appointment,
            reason=SCHEDULED,
            report_datetime=report_datetime or next_appointment.appt_datetime,
            visit_code=next_appointment.visit_code,
            visit_code_sequence=next_appointment.visit_code_sequence,
        )
        next_subject_visit.save()
        next_subject_visit.refresh_from_db()
        return next_subject_visit

    @staticmethod
    def get_or_create_clinical_review_baseline(
        patient_log: PatientLog, subject_visit: SubjectVisit
    ) -> ClinicalReviewBaseline:
        cond = [obj.name for obj in patient_log.conditions.all()][0]
        options = {f"{cond.lower()}_dx": YES, f"{cond.lower()}_dx_at_screening": YES}
        try:
            obj = ClinicalReviewBaseline.objects.get(subject_visit=subject_visit)
        except ObjectDoesNotExist:
            for cond in [c for c in [HIV, DM, HTN] if c != cond]:
                options.update(
                    {
                        f"{cond.lower()}_dx": NO,
                        f"{cond.lower()}_dx_at_screening": NOT_APPLICABLE,
                    }
                )
            obj = baker.make_recipe(
                "intecomm_subject.clinicalreviewbaseline",
                subject_visit=subject_visit,
                report_datetime=subject_visit.report_datetime,
                **options,
            )
        return obj

    @staticmethod
    def get_or_create_clinical_review(
        patient_log: PatientLog, subject_visit: SubjectVisit
    ) -> ClinicalReview:
        cond = [obj.name for obj in patient_log.conditions.all()][0]
        options = {f"{cond.lower()}_dx": YES}
        try:
            obj = ClinicalReview.objects.get(subject_visit=subject_visit)
        except ObjectDoesNotExist:
            for cond in [c for c in [HIV, DM, HTN] if c != cond]:
                options.update({f"{cond.lower()}_dx": NO})
            obj = baker.make_recipe(
                "intecomm_subject.clinicalreview",
                subject_visit=subject_visit,
                report_datetime=subject_visit.report_datetime,
                **options,
            )
        return obj
