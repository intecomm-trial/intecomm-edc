from dateutil.relativedelta import relativedelta
from edc_constants.constants import BLACK, FEMALE, NO, NOT_APPLICABLE, YES
from edc_utils import get_utcnow
from faker import Faker
from model_bakery.recipe import Recipe

from .models import SubjectScreening

fake = Faker()


subjectscreening = Recipe(
    SubjectScreening,
    report_datetime=get_utcnow() - relativedelta(days=1),
    screening_consent=YES,
    hospital_identifier="111",
    initials="ZZ",
    subject_identifier=None,
    gender=FEMALE,
    age_in_years=40,
    ethnicity=BLACK,
    unsuitable_for_study=NO,
    unsuitable_agreed=NOT_APPLICABLE,
)
