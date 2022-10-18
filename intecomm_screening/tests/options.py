from datetime import datetime
from secrets import choice

import arrow
from dateutil.relativedelta import relativedelta
from edc_constants.constants import FEMALE, YES
from edc_reportable import MILLIMOLES_PER_LITER
from faker import Faker
from pyparsing import alphas

fake = Faker()
now = arrow.get(datetime(2019, 5, 5), "UTC").datetime
tomorrow = now + relativedelta(days=1)


def get_eligible_options() -> dict:
    return dict(
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
        dia_blood_pressure=80,
        fasting=YES,
        fasting_duration_str="8h",
        fbg_datetime=now,
        fbg_units=MILLIMOLES_PER_LITER,
        fbg_value=11.0,
        sys_blood_pressure=120,
        reasons_unsuitable=None,
    )
