def get_search_fields(include_pii=None):
    search_fields = [
        "id",
        "screening_identifier",
        "subject_identifier",
        "hospital_identifier__exact",
        "initials__exact",
        "filing_identifier",
        "patient_log_identifier",
        "group_identifier",
        "contact_number__exact",
        "alt_contact_number__exact",
        "last_4_hospital_identifier__exact",
        "last_4_contact_number__exact",
    ]
    if include_pii:
        search_fields.extend(
            [
                "legal_name__exact",
                "familiar_name__exact",
            ]
        )
    return tuple(search_fields)
