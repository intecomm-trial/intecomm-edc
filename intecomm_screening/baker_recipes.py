from uuid import uuid4

from dateutil.relativedelta import relativedelta
from edc_constants.constants import BLACK, FEMALE, NO, NOT_APPLICABLE, YES
from edc_utils import get_utcnow
from faker import Faker
from model_bakery.recipe import Recipe

from .models import PatientLog, SubjectScreening

fake = Faker()

name = fake.name()
names = name.split(" ")
firstname = names[0].upper()
lastname = names[-1].upper()
initials = f"{firstname[0]}{lastname[0]}".upper()


patientlog = Recipe(
    PatientLog,
    report_datetime=get_utcnow(),
    hf_identifier="123456789",
    patient_log_identifier=uuid4(),
    # site=101,
    name=f"{firstname} {lastname}",
    initials=initials,
    contact_number="765456",
    gender=FEMALE,
    may_contact=YES,
)

subjectscreening = Recipe(
    SubjectScreening,
    report_datetime=get_utcnow() - relativedelta(days=1),
    screening_consent=YES,
    hospital_identifier="123456789",
    initials=initials,
    subject_identifier=None,
    gender=FEMALE,
    age_in_years=40,
    ethnicity=BLACK,
    unsuitable_for_study=NO,
    unsuitable_agreed=NOT_APPLICABLE,
)
