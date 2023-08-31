def get_first_fieldset():
    return (
        None,
        {
            "fields": (
                "patient_log_identifier",
                "filing_identifier",
                "report_datetime",
                "site",
            )
        },
    )


def get_names_and_basic_demographics_fieldset(include_pii=None):
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
        "Name and basic demographics",
        {"fields": tuple(fields)},
    )


def get_contact_fieldset():
    return (
        "Contact",
        {
            "fields": (
                "contact_number",
                "alt_contact_number",
                "may_contact",
            )
        },
    )


def get_address_fielset():
    return (
        "Address / Location",
        {"fields": ("location_description",)},
    )


def get_health_fieldset():
    return (
        "Health",
        {
            "description": "Select one or more conditions with a documented diagnoses",
            "fields": (
                "conditions",
                "stable",
            ),
        },
    )


def get_health_talks_fieldset():
    return (
        "Health talks",
        {
            "fields": (
                "first_health_talk",
                "first_health_talk_date",
                "second_health_talk",
                "second_health_talk_date",
            )
        },
    )


def get_appointment_fieldset():
    return (
        "Appointments",
        {
            "fields": (
                "last_appt_date",
                "next_appt_date",
            )
        },
    )


def get_willingness_to_screen_fieldset():
    return (
        "Willingness to screen",
        {
            "description": (
                "This section may be left blank until a decision is made. If and when the "
                "screening form is submitted, the response here will be "
                "automatically updated by the EDC"
            ),
            "fields": (
                "willing_to_screen",
                "screening_refusal_reason",
                "screening_refusal_reason_other",
            ),
        },
    )


def get_screening_and_consent_fieldset():
    return (
        "Screening and Consent",
        {
            "classes": ("collapse",),
            "fields": (
                "comment",
                "screening_identifier",
                "screening_datetime",
                "subject_identifier",
                "consent_datetime",
            ),
        },
    )


def get_group_fieldset():
    return (
        "Group",
        {"classes": ("collapse",), "fields": ("group_identifier",)},
    )
