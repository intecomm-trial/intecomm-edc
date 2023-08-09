import datetime as dt
from zoneinfo import ZoneInfo

import time_machine
from dateutil.relativedelta import relativedelta
from django.core.management import call_command
from django.test import TestCase, tag
from edc_constants.constants import (
    COMPLETE,
    DM,
    FEMALE,
    HTN,
    MALE,
    NO,
    NOT_APPLICABLE,
    YES,
)
from edc_he.constants import WIFE_HUSBAND
from edc_he.forms import HealthEconomicsHouseholdHeadForm
from edc_he.models import (
    Education,
    EmploymentType,
    Ethnicities,
    InsuranceTypes,
    Religions,
)
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_utils import age, get_utcnow
from edc_visit_schedule.constants import DAY1
from faker import Faker

from intecomm_consent.models import SubjectConsent
from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin
from intecomm_subject.models import ClinicalReviewBaseline, HealthEconomicsHouseholdHead

fake = Faker()


def get_obj(model_cls, name: str = None):
    if name:
        obj = model_cls.objects.get(name=name)
    else:
        obj = model_cls.objects.all()[0]
    return obj


def get_m2m_qs(model_cls, name: str = None):
    if name:
        qs = model_cls.objects.filter(name=name)
    else:
        name = model_cls.objects.all()[0].name
        qs = model_cls.objects.filter(name=name).exclude(name=NOT_APPLICABLE)
    return qs


utc_tz = ZoneInfo("UTC")


@time_machine.travel(dt.datetime(2019, 5, 11, 8, 00, tzinfo=utc_tz))
class TestHe(IntecommTestCaseMixin, TestCase):
    patient_group = None

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.patient_group = cls.get_randomized_patient_group(
            report_datetime=get_utcnow() - relativedelta(days=10)
        )

    def setUp(self):
        self.assertTrue(self.patient_group.randomized)
        ClinicalReviewBaseline.objects.all().delete()
        HealthEconomicsHouseholdHead.objects.all().delete()
        call_command("update_metadata")

    def test_with_models(self):
        patient_log = self.patient_group.patients.filter(conditions__name__in=[DM]).first()
        subject_visit = self.get_subject_visit(
            subject_identifier=patient_log.subject_identifier
        )
        traveller = time_machine.travel(subject_visit.report_datetime)
        traveller.start()
        self.create_clinical_review_baseline(patient_log, subject_visit)
        hoh_obj = HealthEconomicsHouseholdHead.objects.create(
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            hh_count=4,
            hh_minors_count=1,
            hoh=NO,
            hoh_gender=MALE,
            hoh_age=52,
            relationship_to_hoh=WIFE_HUSBAND,
            hoh_employment_status="1",
            hoh_marital_status="1",
            hoh_religion=get_obj(Religions),
            hoh_ethnicity=get_obj(Ethnicities),
            hoh_education=get_obj(Education),
            hoh_employment_type=get_obj(EmploymentType),
        )
        hoh_obj.hoh_insurance.add(get_obj(InsuranceTypes))
        qs = CrfMetadata.objects.filter(
            model="intecomm_subject.healtheconomicspatient",
            entry_status=REQUIRED,
            visit_code=DAY1,
            subject_identifier=patient_log.subject_identifier,
        )
        self.assertTrue(qs.exists())

        hoh_obj.hoh = YES
        hoh_obj.hoh_gender = patient_log.gender
        hoh_obj.hoh_age = patient_log.age_in_years
        hoh_obj.relationship_to_hoh = NOT_APPLICABLE
        hoh_obj.hoh_employment_status = NOT_APPLICABLE
        hoh_obj.hoh_marital_status = NOT_APPLICABLE
        hoh_obj.hoh_religion = get_obj(Religions, NOT_APPLICABLE)
        hoh_obj.hoh_ethnicity = get_obj(Ethnicities, NOT_APPLICABLE)
        hoh_obj.hoh_education = get_obj(Education, NOT_APPLICABLE)
        hoh_obj.hoh_employment_type = get_obj(EmploymentType, NOT_APPLICABLE)
        hoh_obj.save()

        qs = CrfMetadata.objects.filter(
            model="intecomm_subject.healtheconomicspatient",
            entry_status=NOT_REQUIRED,
            visit_code=DAY1,
            subject_identifier=patient_log.subject_identifier,
        )
        self.assertTrue(qs.exists())

    @tag("1")
    def test_with_forms(self):
        patient_log = self.patient_group.patients.filter(conditions__name__in=[HTN]).first()
        subject_visit = self.get_subject_visit(
            subject_identifier=patient_log.subject_identifier
        )
        traveller = time_machine.travel(subject_visit.report_datetime)
        traveller.start()

        cleaned_data = dict(
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            hh_count=4,
            hh_minors_count=1,
            hoh=YES,
            hoh_gender=MALE,
            hoh_age=52,
            relationship_to_hoh=NOT_APPLICABLE,
            hoh_employment_status=NOT_APPLICABLE,
            hoh_marital_status=NOT_APPLICABLE,
            hoh_religion=get_obj(Religions, NOT_APPLICABLE),
            hoh_ethnicity=get_obj(Ethnicities, NOT_APPLICABLE),
            hoh_education=get_obj(Education, NOT_APPLICABLE),
            hoh_employment_type=get_obj(EmploymentType, NOT_APPLICABLE),
            hoh_insurance=get_m2m_qs(InsuranceTypes, NOT_APPLICABLE),
            crf_status=COMPLETE,
        )
        # try before submitting required ClinicalReviewBaseline
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn(
            ClinicalReviewBaseline._meta.verbose_name, str(form.errors.get("__all__"))
        )

        self.create_clinical_review_baseline(patient_log, subject_visit)

        # submit where patient is HOH but wrong gender
        subject_consent = SubjectConsent.objects.get(
            subject_identifier=patient_log.subject_identifier
        )
        cleaned_data.update(
            hoh_gender=MALE if patient_log.gender == FEMALE else MALE,
            hoh_age=age(subject_consent.dob, get_utcnow(), timezone="utc").years,
        )
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_gender", form._errors)

        # submit where patient is HOH but wrong age
        cleaned_data.update(
            hoh_gender=patient_log.gender,
            hoh_age=age(subject_consent.dob, get_utcnow(), timezone="utc").years - 5,
        )
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_age", form._errors)

        # submit where patient is HOH ok
        cleaned_data.update(
            hoh_gender=patient_log.gender,
            hoh_age=age(subject_consent.dob, get_utcnow(), timezone="utc").years,
        )
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertEqual({}, form._errors)

        # submit where patient is not HOH
        cleaned_data = dict(
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            hh_count=4,
            hh_minors_count=1,
            hoh=NO,
            relationship_to_hoh=NOT_APPLICABLE,
            hoh_employment_status=NOT_APPLICABLE,
            hoh_marital_status=NOT_APPLICABLE,
            hoh_religion=get_obj(Religions, NOT_APPLICABLE),
            hoh_ethnicity=get_obj(Ethnicities, NOT_APPLICABLE),
            hoh_education=get_obj(Education, NOT_APPLICABLE),
            hoh_employment_type=get_obj(EmploymentType, NOT_APPLICABLE),
            hoh_insurance=get_m2m_qs(InsuranceTypes, NOT_APPLICABLE),
            crf_status=COMPLETE,
        )
        cleaned_data.update(hoh_gender=MALE, hoh_age=75)
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("relationship_to_hoh", form._errors)

        cleaned_data.update(
            relationship_to_hoh=WIFE_HUSBAND,
        )
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_employment_status", form._errors)

        cleaned_data.update(hoh_employment_status="1")
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_marital_status", form._errors)

        cleaned_data.update(hoh_marital_status="1")
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_religion", form._errors)

        cleaned_data.update(hoh_religion=get_obj(Religions))
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_ethnicity", form._errors)

        cleaned_data.update(hoh_ethnicity=get_obj(Ethnicities))
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_education", form._errors)

        cleaned_data.update(hoh_education=get_obj(Education))
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_employment_type", form._errors)

        cleaned_data.update(hoh_employment_type=get_obj(EmploymentType))
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_insurance_type", form._errors)
