from edc_auth.get_clinic_codenames import get_clinic_codenames

clinic_codenames = get_clinic_codenames(
    "intecomm_prn", "intecomm_subject", "intecomm_consent", list_app="intecomm_lists"
)

screening_codenames = [
    "intecomm_screening.add_subjectscreening",
    "intecomm_screening.change_subjectscreening",
    "intecomm_screening.delete_subjectscreening",
    "intecomm_screening.view_subjectscreening",
    "intecomm_screening.add_subjectrefusal",
    "intecomm_screening.change_subjectrefusal",
    "intecomm_screening.delete_subjectrefusal",
    "intecomm_screening.view_subjectrefusal",
    "intecomm_screening.view_historicalsubjectscreening",
    "intecomm_screening.view_historicalsubjectrefusal",
]
screening_codenames.sort()
