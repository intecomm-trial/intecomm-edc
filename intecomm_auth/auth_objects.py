from edc_auth.get_clinic_codenames import get_clinic_codenames

clinic_codenames = get_clinic_codenames(
    "intecomm_prn",
    "intecomm_group",
    "intecomm_subject",
    "intecomm_consent",
    "intecomm_screening",
    list_app="intecomm_lists",
)

screening_codenames = get_clinic_codenames(
    "intecomm_screening",
    list_app="intecomm_lists",
)
screening_codenames.sort()
