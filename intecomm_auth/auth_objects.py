from edc_auth.get_clinic_codenames import get_clinic_codenames

clinic_codenames = get_clinic_codenames(
    "intecomm_prn",
    "intecomm_group",
    "intecomm_subject",
    "intecomm_consent",
    "intecomm_screening",
    "edc_qol",
    list_app="intecomm_lists",
)

# remove any user from deleting a patient group
clinic_codenames = [
    codename for codename in clinic_codenames if not codename.endswith("delete_patientgroup")
]
screening_codenames = get_clinic_codenames(
    "intecomm_screening",
    list_app="intecomm_lists",
)
screening_codenames = [
    codename
    for codename in screening_codenames
    if not codename.endswith("delete_patientgroup")
]

screening_codenames.sort()
