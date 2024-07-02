from edc_auth.get_app_codenames import get_app_codenames

INTECOMM_REPORTS = "INTECOMM_REPORTS"
INTECOMM_REPORTS_AUDIT = "INTECOMM_REPORTS_AUDIT"

clinic_codenames = get_app_codenames(
    "intecomm_prn",
    "intecomm_group",
    "intecomm_subject",
    "intecomm_consent",
    "intecomm_screening",
    "intecomm_facility",
    "edc_qol",
    list_app="intecomm_lists",
)

# remove any user from deleting a patient group
clinic_codenames = [
    codename
    for codename in clinic_codenames
    if not codename.endswith("delete_patientgroup")
    and not codename.endswith("delete_patientgrouprando")
    and not codename.endswith("add_patientgrouprando")
    and codename != "intecomm_group.add_patientgroup"
    and codename != "intecomm_group.change_patientgroup"
]
screening_codenames = get_app_codenames(
    "intecomm_screening",
    list_app="intecomm_lists",
)
screening_codenames = [
    codename
    for codename in screening_codenames
    if not codename.endswith("delete_patientgroup")
    and not codename.endswith("delete_patientgrouprando")
    and not codename.endswith("add_patientgrouprando")
    and codename != "intecomm_group.add_patientgroup"
    and codename != "intecomm_group.change_patientgroup"
]

screening_codenames.sort()

reports_codenames = [c for c in get_app_codenames("intecomm_reports")]
