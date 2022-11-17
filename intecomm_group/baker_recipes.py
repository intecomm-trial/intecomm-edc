from dateutil.relativedelta import relativedelta
from edc_constants.constants import MALE, NO, YES
from edc_utils import get_utcnow
from faker import Faker
from intecomm_form_validators import RECRUITING
from model_bakery.recipe import Recipe

from .models import PatientGroup, PatientLog

fake = Faker()

name = fake.name()
names = name.split(" ")
firstname = names[0].upper()
lastname = names[-1].upper()
initials = f"{firstname[0]}{lastname[0]}".upper()


patientgroup = Recipe(
    PatientGroup,
    report_datetime=get_utcnow(),
    status=RECRUITING,
    randomize_now=NO,
)

patientlog = Recipe(
    PatientLog,
    report_datetime=get_utcnow(),
    screening_identifier=None,
    subject_identifier=None,
    consent_datetime=None,
    gender=MALE,
    may_contact=YES,
    stable=YES,
    last_routine_appt_date=get_utcnow() - relativedelta(months=1),
    next_routine_appt_date=get_utcnow() + relativedelta(months=1),
    first_health_talk=YES,
    second_health_talk=YES,
    call_attempts=1,
)
