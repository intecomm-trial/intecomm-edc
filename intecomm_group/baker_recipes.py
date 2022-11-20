from edc_constants.constants import NO
from edc_utils import get_utcnow
from faker import Faker
from intecomm_form_validators import RECRUITING
from model_bakery.recipe import Recipe

from .models import PatientGroup

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
