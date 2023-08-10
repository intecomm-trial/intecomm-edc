from dateutil.relativedelta import relativedelta
from edc_constants.constants import EQ, NO, NOT_APPLICABLE, YES
from edc_dx_review.constants import THIS_CLINIC
from edc_utils import get_utcnow
from faker import Faker
from model_bakery.recipe import Recipe

from .models import (
    ClinicalReview,
    ClinicalReviewBaseline,
    DmInitialReview,
    DmReview,
    HealthEconomicsHouseholdHead,
    HivInitialReview,
    HivReview,
    HtnInitialReview,
    HtnReview,
)

fake = Faker()

clinicalreviewbaseline = Recipe(
    ClinicalReviewBaseline,
    report_datetime=get_utcnow(),
    hiv_dx=NO,
    hiv_dx_at_screening=NOT_APPLICABLE,
    dm_dx=NO,
    dm_dx_at_screening=NOT_APPLICABLE,
    htn_dx=NO,
    htn_dx_at_screening=NOT_APPLICABLE,
)

clinicalreview = Recipe(
    ClinicalReview,
    report_datetime=get_utcnow(),
    hiv_test=NO,
    hiv_test_date=None,
    htn_test=NO,
    htn_test_date=None,
    dm_test=NO,
    dm_test_date=None,
)


hivinitialreview = Recipe(
    HivInitialReview,
    report_datetime=get_utcnow(),
    receives_care=YES,
    clinic=THIS_CLINIC,
    has_vl=YES,
    vl=50,
    vl_quantifier=EQ,
    drawn_date=(get_utcnow() - relativedelta(months=5)).date(),
    has_cd4=NO,
)

dminitialreview = Recipe(
    DmInitialReview,
    report_datetime=get_utcnow(),
)

htninitialreview = Recipe(
    HtnInitialReview, report_datetime=get_utcnow(), rx_init_date_is_estimated=NO
)


hivreview = Recipe(
    HivReview,
    report_datetime=get_utcnow(),
)

dmreview = Recipe(
    DmReview,
    report_datetime=get_utcnow(),
)

htnreview = Recipe(
    HtnReview,
    report_datetime=get_utcnow(),
)

healtheconomicshouseholdhead = Recipe(
    HealthEconomicsHouseholdHead,
    report_datetime=get_utcnow(),
)
