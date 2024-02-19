from __future__ import annotations

import datetime as dt
from zoneinfo import ZoneInfo

import time_machine
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.test import TestCase
from edc_constants.constants import COMPLETE, DM, HTN, MALE, NO, NOT_APPLICABLE, YES
from edc_he.constants import WIFE_HUSBAND
from edc_he.models import (
    Education,
    EmploymentType,
    Ethnicities,
    InsuranceTypes,
    Religions,
)
from edc_metadata import KEYED, NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_metadata.utils import refresh_metadata_for_timepoint
from edc_utils import get_utcnow
from edc_visit_schedule.constants import DAY1
from faker import Faker

from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin
from intecomm_subject.forms import (
    HealthEconomicsHouseholdHeadForm,
    HealthEconomicsPatientForm,
)
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


@time_machine.travel(dt.datetime(2023, 8, 11, 8, 00, tzinfo=utc_tz))
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

    @staticmethod
    def get_hoh_options(not_applicable: str | None = None) -> dict:
        if not_applicable:
            opts = dict(
                relationship_to_hoh=NOT_APPLICABLE,
                hoh_employment_status=NOT_APPLICABLE,
                hoh_marital_status=NOT_APPLICABLE,
                hoh_religion=get_obj(Religions, NOT_APPLICABLE),
                hoh_ethnicity=get_obj(Ethnicities, NOT_APPLICABLE),
                hoh_education=get_obj(Education, NOT_APPLICABLE),
                hoh_employment_type=get_obj(EmploymentType, NOT_APPLICABLE),
                hoh_insurance=get_m2m_qs(InsuranceTypes, NOT_APPLICABLE),
                crf_status=COMPLETE,
                site=Site.objects.get(id=settings.SITE_ID),
            )
        else:
            opts = dict(
                relationship_to_hoh=WIFE_HUSBAND,
                hoh_employment_status="1",
                hoh_marital_status="1",
                hoh_religion=get_obj(Religions),
                hoh_ethnicity=get_obj(Ethnicities),
                hoh_education=get_obj(Education),
                hoh_employment_type=get_obj(EmploymentType),
                hoh_insurance=get_m2m_qs(InsuranceTypes),
                crf_status=COMPLETE,
                site=Site.objects.get(id=settings.SITE_ID),
            )
        return opts

    def test_with_models(self):
        ClinicalReviewBaseline.objects.all().delete()
        HealthEconomicsHouseholdHead.objects.all().delete()
        call_command("update_metadata")
        patient_log = self.patient_group.patients.filter(conditions__name__in=[DM]).first()
        subject_visit = self.get_subject_visit(
            subject_identifier=patient_log.subject_identifier
        )
        traveller = time_machine.travel(subject_visit.report_datetime)
        traveller.start()
        self.get_or_create_clinical_review_baseline(patient_log, subject_visit)
        opts = dict(
            hoh=NO,
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            hh_count=4,
            hh_minors_count=1,
            hoh_gender=MALE,
            hoh_age=52,
            **self.get_hoh_options(),
        )
        del opts["hoh_insurance"]
        hoh_obj = HealthEconomicsHouseholdHead.objects.create(**opts)
        hoh_obj.hoh_insurance.add(get_obj(InsuranceTypes))
        qs = CrfMetadata.objects.filter(
            model="intecomm_subject.healtheconomicspatient",
            entry_status=NOT_REQUIRED,
            visit_code=DAY1,
            subject_identifier=patient_log.subject_identifier,
        )
        self.assertTrue(qs.exists())

        hoh_obj.hoh = YES
        hoh_obj.hoh_gender = NOT_APPLICABLE
        hoh_obj.hoh_age = None
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
            entry_status=REQUIRED,
            visit_code=DAY1,
            subject_identifier=patient_log.subject_identifier,
        )
        self.assertTrue(qs.exists())

    def test_with_forms_is_hoh(self):
        """Assert if patient is Head of Household, complete Head of Household data on
        Patient form, not on the Head of Household form.
        """
        ClinicalReviewBaseline.objects.all().delete()
        HealthEconomicsHouseholdHead.objects.all().delete()
        call_command("update_metadata")
        patient_log = self.patient_group.patients.filter(conditions__name__in=[HTN]).first()
        subject_visit = self.get_subject_visit(
            subject_identifier=patient_log.subject_identifier
        )

        traveller = time_machine.travel(subject_visit.report_datetime)
        traveller.start()
        self.get_or_create_clinical_review_baseline(patient_log, subject_visit)
        cleaned_data = dict(
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            hh_count=4,
            hh_minors_count=1,
            hoh=YES,  # patient is HoH
            hoh_gender=NOT_APPLICABLE,
            hoh_age=None,
            **self.get_hoh_options(NOT_APPLICABLE),
        )
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertEqual({}, form._errors)

        cleaned_data.update(relationship_to_hoh=WIFE_HUSBAND)
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("relationship_to_hoh", form._errors)
        cleaned_data.update(relationship_to_hoh=NOT_APPLICABLE)

        cleaned_data.update(hoh_religion=get_obj(Religions))
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_religion", form._errors)
        cleaned_data.update(hoh_religion=get_obj(Religions, NOT_APPLICABLE))

        cleaned_data.update(hoh_ethnicity=get_obj(Ethnicities))
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_ethnicity", form._errors)
        cleaned_data.update(hoh_ethnicity=get_obj(Ethnicities, NOT_APPLICABLE))

        cleaned_data.update(hoh_education=get_obj(Education))
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_education", form._errors)
        cleaned_data.update(hoh_education=get_obj(Education, NOT_APPLICABLE))

        cleaned_data.update(hoh_employment_status="1")
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_employment_status", form._errors)
        cleaned_data.update(hoh_employment_status=NOT_APPLICABLE)

        cleaned_data.update(hoh_employment_type=get_obj(EmploymentType))
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_employment_type", form._errors)
        cleaned_data.update(hoh_employment_type=get_obj(EmploymentType, NOT_APPLICABLE))

        cleaned_data.update(hoh_marital_status="1")
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_marital_status", form._errors)
        cleaned_data.update(hoh_marital_status=NOT_APPLICABLE)

        cleaned_data.update(hoh_insurance=get_m2m_qs(InsuranceTypes))
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_insurance", form._errors)
        cleaned_data.update(hoh_insurance=get_m2m_qs(InsuranceTypes, NOT_APPLICABLE))

        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertEqual({}, form._errors)

    def test_with_forms_is_not_hoh(self):
        ClinicalReviewBaseline.objects.all().delete()
        HealthEconomicsHouseholdHead.objects.all().delete()
        call_command("update_metadata")
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
            hoh=NO,  # patient is not HoH
            hoh_gender=MALE,
            hoh_age=52,
            **self.get_hoh_options(),
        )

        self.get_or_create_clinical_review_baseline(patient_log, subject_visit)
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertEqual({}, form._errors)

        cleaned_data.update(relationship_to_hoh=NOT_APPLICABLE)
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("relationship_to_hoh", form._errors)
        cleaned_data.update(relationship_to_hoh=WIFE_HUSBAND)

        cleaned_data.update(hoh_religion=get_obj(Religions, NOT_APPLICABLE))
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_religion", form._errors)
        cleaned_data.update(hoh_religion=get_obj(Religions))

        cleaned_data.update(hoh_ethnicity=get_obj(Ethnicities, NOT_APPLICABLE))
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_ethnicity", form._errors)
        cleaned_data.update(hoh_ethnicity=get_obj(Ethnicities))

        cleaned_data.update(hoh_education=get_obj(Education, NOT_APPLICABLE))
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_education", form._errors)
        cleaned_data.update(hoh_education=get_obj(Education))

        cleaned_data.update(hoh_employment_status=NOT_APPLICABLE)
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_employment_status", form._errors)
        cleaned_data.update(hoh_employment_status="1")

        cleaned_data.update(hoh_employment_type=get_obj(EmploymentType, NOT_APPLICABLE))
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_employment_type", form._errors)
        cleaned_data.update(hoh_employment_type=get_obj(EmploymentType))

        cleaned_data.update(hoh_marital_status=NOT_APPLICABLE)
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_marital_status", form._errors)
        cleaned_data.update(hoh_marital_status="1")

        cleaned_data.update(hoh_insurance=get_m2m_qs(InsuranceTypes, NOT_APPLICABLE))
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn("hoh_insurance", form._errors)
        cleaned_data.update(hoh_insurance=get_m2m_qs(InsuranceTypes))

        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertEqual({}, form._errors)

    def test_entered_across_visits(self):
        ClinicalReviewBaseline.objects.all().delete()
        HealthEconomicsHouseholdHead.objects.all().delete()
        call_command("update_metadata")
        patient_log = self.patient_group.patients.filter(conditions__name__in=[HTN]).first()
        subject_visit = self.get_subject_visit(
            subject_identifier=patient_log.subject_identifier
        )
        traveller = time_machine.travel(subject_visit.report_datetime)
        traveller.start()
        self.get_or_create_clinical_review_baseline(patient_log, subject_visit)
        cleaned_data = dict(
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            hh_count=4,
            hh_minors_count=1,
            hoh=YES,  # patient is HoH
            hoh_gender=NOT_APPLICABLE,
            hoh_age=None,
            **self.get_hoh_options(NOT_APPLICABLE),
        )
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertEqual({}, form._errors)
        form.save(commit=True)

        qs = CrfMetadata.objects.filter(
            model="intecomm_subject.healtheconomicshouseholdhead",
            entry_status=KEYED,
            visit_code=subject_visit.visit_code,
            subject_identifier=patient_log.subject_identifier,
        )
        self.assertTrue(qs.exists())

        refresh_metadata_for_timepoint(subject_visit)

        qs = CrfMetadata.objects.filter(
            model="intecomm_subject.healtheconomicspatient",
            entry_status=REQUIRED,
            visit_code=subject_visit.visit_code,
            subject_identifier=patient_log.subject_identifier,
        )
        self.assertTrue(qs.exists())

        subject_visit = self.get_next_subject_visit(subject_visit)
        traveller = time_machine.travel(subject_visit.report_datetime)
        traveller.start()

        qs = CrfMetadata.objects.filter(
            model="intecomm_subject.healtheconomicshouseholdhead",
            entry_status=NOT_REQUIRED,
            visit_code=subject_visit.visit_code,
            subject_identifier=patient_log.subject_identifier,
        )
        self.assertTrue(qs.exists())

        qs = CrfMetadata.objects.filter(
            model="intecomm_subject.healtheconomicspatient",
            entry_status=REQUIRED,
            visit_code=subject_visit.visit_code,
            subject_identifier=patient_log.subject_identifier,
        )
        self.assertTrue(qs.exists())

        cleaned_data.update(
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
        )
        form = HealthEconomicsHouseholdHeadForm(data=cleaned_data)
        form.is_valid()
        self.assertIn(
            "This form has already been submitted",
            str(form._errors.get("__all__")),
        )

        cleaned_data = dict(
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            pat_religion=get_obj(Religions),
            pat_ethnicity=get_obj(Ethnicities),
            pat_education=get_obj(Education),
            pat_employment_status="1",
            pat_employment_type=get_obj(EmploymentType),
            pat_marital_status="1",
            pat_insurance=get_m2m_qs(InsuranceTypes),
            crf_status=COMPLETE,
            site=Site.objects.get(id=settings.SITE_ID),
        )
        form = HealthEconomicsPatientForm(data=cleaned_data)
        form.is_valid()

        self.assertIn("Complete Clinical Review CRF first", form._errors.get("__all__")[0])

        self.get_or_create_clinical_review(patient_log, subject_visit)

        form = HealthEconomicsPatientForm(data=cleaned_data)
        form.is_valid()
        self.assertEqual({}, form._errors)
        form.save(commit=True)

        qs = CrfMetadata.objects.filter(
            model="intecomm_subject.healtheconomicspatient",
            entry_status=KEYED,
            visit_code=subject_visit.visit_code,
            subject_identifier=patient_log.subject_identifier,
        )
        self.assertTrue(qs.exists())

        qs = CrfMetadata.objects.filter(
            model="intecomm_subject.healtheconomicspatient",
            entry_status=NOT_REQUIRED,
            visit_code=subject_visit.previous_visit.visit_code,
            subject_identifier=patient_log.subject_identifier,
        )
        self.assertTrue(qs.exists())
