from datetime import datetime
from random import sample
from secrets import choice

import arrow
from dateutil.relativedelta import relativedelta
from edc_constants.constants import (
    BLACK,
    FEMALE,
    NO,
    NOT_APPLICABLE,
    RANDOM_SAMPLING,
    TBD,
    YES,
)
from edc_reportable.units import MICROMOLES_PER_LITER, MILLIMOLES_PER_LITER
from faker import Faker
from pyparsing import alphas

from intecomm_screening.forms import get_part_one_fields, get_part_two_fields

fake = Faker()
now = arrow.get(datetime(2019, 5, 5), "UTC").datetime
tomorrow = now + relativedelta(days=1)


def get_part_one_eligible_options():
    options = dict(
        age_in_years=25,
        art_six_months=YES,
        continue_part_two=YES,
        ethnicity=BLACK,
        gender=FEMALE,
        hiv_pos=YES,
        hospital_identifier="".join(map(str, sample(range(0, 10), 10))),
        initials=f"{choice(alphas)}{choice(alphas)}".upper(),
        lives_nearby=YES,
        on_rx_stable=YES,
        pregnant=NOT_APPLICABLE,
        report_datetime=now,
        screening_consent=YES,
        selection_method=RANDOM_SAMPLING,
        staying_nearby_6=YES,
    )
    if fld := [f for f in get_part_one_fields() if f not in options]:
        raise TypeError(f"Missing part one fields. Got {fld}.")
    return options


def get_part_two_eligible_options():
    options = dict(
        acute_condition=NO,
        acute_metabolic_acidosis=NO,
        advised_to_fast=YES,
        alcoholism=NO,
        already_fasted=NO,
        appt_datetime=now + relativedelta(days=1),
        congestive_heart_failure=NO,
        liver_disease=NO,
        metformin_sensitivity=NO,
        part_two_report_datetime=now,
        renal_function_condition=NO,
        tissue_hypoxia_condition=NO,
    )
    if fld := [f for f in get_part_two_fields() if f not in options]:
        raise TypeError(f"Missing part two fields. Got {fld}.")
    return options
