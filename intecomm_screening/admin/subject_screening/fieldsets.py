def get_first_fieldset():
    return (
        None,
        {
            "fields": (
                "report_datetime",
                "site",
                "patient_log_identifier",
            )
        },
    )


def get_demographics_fieldset(include_pii=None):
    fields = []
    if include_pii:
        fields.extend(["legal_name", "familiar_name"])
    fields.extend(
        [
            "initials",
            "hospital_identifier",
            "gender",
            "age_in_years",
        ]
    )
    return (
        "Demographics",
        {
            "description": (
                "Please review carefully. If anything needs to be changed, do so on "
                "the Patient Log and try again"
            ),
            "fields": tuple(fields),
        },
    )


def get_health_facility_fieldset():
    return (
        "Health facility",
        {
            "fields": (
                "in_care_6m",
                "in_care_duration",
            )
        },
    )


def get_hiv_fieldset():
    return (
        "HIV",
        {
            "fields": (
                "hiv_dx",
                "hiv_dx_6m",
                "hiv_dx_ago",
                "art_unchanged_3m",
                "art_stable",
                "art_adherent",
            )
        },
    )


def get_dm_fieldset():
    return (
        "Diabetes",
        {
            "fields": (
                "dm_dx",
                "dm_dx_6m",
                "dm_dx_ago",
                "dm_complications",
            )
        },
    )


def get_htn_fieldset():
    return (
        "Hypertension",
        {
            "fields": (
                "htn_dx",
                "htn_dx_6m",
                "htn_dx_ago",
                "htn_complications",
            )
        },
    )


def get_pregnancy_fieldset():
    return (
        "Pregnancy",
        {"fields": ("pregnant",)},
    )


def get_other_history_fieldset():
    return (
        "Other history",
        {
            "fields": (
                "excluded_by_bp_history",
                "excluded_by_gluc_history",
                "requires_acute_care",
            )
        },
    )


def get_location_fieldset():
    return (
        "Location",
        {
            "fields": (
                "lives_nearby",
                "staying_nearby_6",
            )
        },
    )


def get_bp_fieldset():
    return (
        "Blood pressure measurements",
        {
            "fields": (
                "sys_blood_pressure_one",
                "dia_blood_pressure_one",
                "sys_blood_pressure_two",
                "dia_blood_pressure_two",
            )
        },
    )


def get_other_fieldset():
    return (
        "Other",
        {
            "fields": (
                "consent_ability",
                "unsuitable_for_study",
                "reasons_unsuitable",
                "unsuitable_agreed",
            )
        },
    )


def get_updates_fieldset():
    return (
        "Updates",
        {
            "classes": ("collapse",),
            "fields": (
                "screening_identifier",
                "eligible",
                "eligibility_datetime",
                "real_eligibility_datetime",
                "reasons_ineligible",
                "subject_identifier",
            ),
        },
    )
