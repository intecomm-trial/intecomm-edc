from datetime import datetime
from secrets import choice

import arrow
from dateutil.relativedelta import relativedelta
from edc_constants.constants import FEMALE, YES
from edc_reportable import MILLIMOLES_PER_LITER
from faker import Faker
from pyparsing import alphas

from intecomm_screening.forms import get_part_one_fields, get_part_two_fields

fake = Faker()
now = arrow.get(datetime(2019, 5, 5), "UTC").datetime
tomorrow = now + relativedelta(days=1)


def get_part_one_eligible_options():
    options = dict(
        age_in_years=25,
        continue_part_two=YES,
        gender=FEMALE,
        patient_conditions=YES,
        fasted=YES,
        initials=f"{choice(alphas)}{choice(alphas)}".upper(),
        report_datetime=now,
        appt_datetime=now,
        screening_consent=YES,
        staying_nearby_6=YES,
    )
    if fld := [f for f in get_part_one_fields() if f not in options]:
        raise TypeError(f"Missing part one fields. Got {fld}.")
    return options


def get_part_two_eligible_options(report_datetime: datetime = None):
    options = dict(
        dia_blood_pressure=65,
        dia_blood_pressure_one=65,
        dia_blood_pressure_two=65,
        fasting=YES,
        fasting_duration_str="8h",
        fbg_datetime=tomorrow,
        fbg_units=MILLIMOLES_PER_LITER,
        fbg_value=6.9,
        part_two_report_datetime=report_datetime or now,
        reasons_unsuitable=None,
        sys_blood_pressure=120,
        sys_blood_pressure_one=120,
        sys_blood_pressure_two=120,
    )
    if fld := [f for f in get_part_two_fields() if f not in options]:
        raise TypeError(f"Missing part two fields. Got {fld}.")
    return options
