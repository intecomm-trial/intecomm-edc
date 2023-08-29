def get_first_fieldset(include_pii=None):
    fields = [
        "screening_identifier",
        "subject_identifier",
    ]
    if include_pii:
        fields.extend(["legal_name", "familiar_name"])
    fields.extend(
        [
            "initials",
            "gender",
            "language",
            "is_literate",
            "witness_name",
            "consent_datetime",
            "dob",
            "is_dob_estimated",
            "identity",
            "identity_type",
            "confirm_identity",
            "is_incarcerated",
        ]
    )
    return (
        None,
        {"fields": tuple(fields)},
    )


def get_review_questions_fieldset():
    return (
        "Review Questions",
        {
            "fields": (
                "consent_reviewed",
                "study_questions",
                "assessment_score",
                "consent_signature",
                "consent_copy",
            ),
            "description": "The following questions are directed to the interviewer.",
        },
    )


def get_group_fieldset():
    return (
        "Group",
        {"classes": ("collapse",), "fields": ("group_identifier",)},
    )
