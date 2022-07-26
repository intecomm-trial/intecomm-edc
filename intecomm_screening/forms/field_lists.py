def get_part_one_fields():
    fields = [
        "report_datetime",
        "screening_consent",
        "initials",
        "gender",
        "age_in_years",
        "patient_conditions",
        "staying_nearby_6",
        "fasted",
        "appt_datetime",
    ]
    return tuple(fields)


def get_part_two_vitals_fields():
    return [
        "sys_blood_pressure_one",
        "dia_blood_pressure_one",
        "sys_blood_pressure_two",
        "dia_blood_pressure_two",
    ]


def get_part_two_fbg_fields():
    return (
        "fasting",
        "fasting_duration_str",
        "fbg_datetime",
        "fbg_value",
        "fbg_units",
    )


def get_part_two_fields():
    fields = [
        "part_two_report_datetime",
        *get_part_two_vitals_fields(),
        *get_part_two_fbg_fields(),
    ]
    return tuple(fields)
