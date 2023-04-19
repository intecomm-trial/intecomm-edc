from dateutil.relativedelta import relativedelta
from edc_constants.constants import MALE, NO, YES
from edc_utils import get_utcnow
from faker import Faker
from intecomm_form_validators import RECRUITING
from model_bakery.recipe import Recipe

from .models import PatientGroup, PatientLog

fake = Faker()

legal_name = fake.name().upper()
familiar_name = legal_name[0].upper()
names = legal_name.split(" ")
initials = f"{names[0][0]}{names[-1][0]}"


patientgroup = Recipe(
    PatientGroup,
    report_datetime=get_utcnow(),
    status=RECRUITING,
    randomize_now=NO,
    group_identifier=None,
)

patientlog = Recipe(
    PatientLog,
    legal_name=legal_name,
    familiar_name=familiar_name,
    initials=initials,
    report_datetime=get_utcnow(),
    screening_identifier=None,
    subject_identifier=None,
    consent_datetime=None,
    gender=MALE,
    may_contact=YES,
    stable=YES,
    last_appt_date=get_utcnow() - relativedelta(months=1),
    next_appt_date=get_utcnow() + relativedelta(months=1),
    first_health_talk=YES,
    second_health_talk=YES,
    call_attempts=1,
)
