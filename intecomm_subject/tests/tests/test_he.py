from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_constants.constants import (
    COMPLETE,
    DM,
    HIV,
    HTN,
    MALE,
    NO,
    NOT_APPLICABLE,
    YES,
)
from edc_he.constants import WIFE_HUSBAND
from edc_he.models import (
    Education,
    EmploymentType,
    Ethnicities,
    InsuranceTypes,
    Religions,
)
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_schedule.constants import DAY1
from edc_visit_tracking.constants import SCHEDULED
from faker import Faker

from intecomm_screening.models import PatientGroupRando, PatientLog
from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin
from intecomm_subject.models import (
    ClinicalReviewBaseline,
    HealthEconomicsHouseholdHead,
    SubjectVisit,
)

fake = Faker()


def get_obj(model_cls, name: str = None):
    if name:
        obj = model_cls.objects.get(name=name)
    else:
        obj = model_cls.objects.all()[0]
    return obj


class TestHe(IntecommTestCaseMixin, TestCase):
    @tag("1")
    def test_ok(self):
        patient_group = self.get_patient_group()

        patient_group.status = COMPLETE
        patient_group.save()
        self.assertEqual(patient_group.status, COMPLETE)

        patient_group = PatientGroupRando.objects.get(id=patient_group.id)
        patient_group.randomize_now = YES
        patient_group.confirm_randomize_now = "RANDOMIZE"
        patient_group.save()
        patient_group.refresh_from_db()
        self.assertTrue(patient_group.randomized)

        appointment = Appointment.objects.filter(visit_code=DAY1)[0]
        subject_visit = SubjectVisit.objects.create(
            appointment=appointment,
            report_datetime=appointment.appt_datetime,
            reason=SCHEDULED,
        )
        patient_log = PatientLog.objects.get(subject_identifier=appointment.subject_identifier)
        cond = [obj.name for obj in patient_log.conditions.all()][0]
        options = {f"{cond.lower()}_dx": YES, f"{cond.lower()}_dx_at_screening": YES}
        for cond in [c for c in [HIV, DM, HTN] if c != cond]:
            options.update({f"{cond.lower()}_dx": NO, f"{cond.lower()}_dx_at_screening": NO})
        ClinicalReviewBaseline.objects.create(
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            **options,
        )
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
