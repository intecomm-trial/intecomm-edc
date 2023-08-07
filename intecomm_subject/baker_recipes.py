from edc_utils import get_utcnow
from faker import Faker
from model_bakery.recipe import Recipe

from intecomm_lists.models import ConsentRefusalReasons

from .models import ClinicalReviewBaseline

fake = Faker()

clinicalreviewbaseline = Recipe(
    ClinicalReviewBaseline,
    report_datetime=get_utcnow(),
    reason=ConsentRefusalReasons.objects.get(name="dont_have_time"),
)
