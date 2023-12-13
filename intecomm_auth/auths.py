from edc_action_item.auth_objects import ACTION_ITEM, ACTION_ITEM_EXPORT
from edc_adverse_event.auth_objects import TMG_ROLE
from edc_appointment.auth_objects import APPOINTMENT_EXPORT
from edc_auth.auth_objects import (
    AUDITOR,
    AUDITOR_ROLE,
    CLINIC,
    CLINIC_SUPER,
    CLINICIAN_ROLE,
    CLINICIAN_SUPER_ROLE,
)
from edc_auth.site_auths import site_auths
from edc_data_manager.auth_objects import DATA_MANAGER_EXPORT, DATA_MANAGER_ROLE
from edc_data_manager.auth_objects import data_manager as data_manager_codenames
from edc_export.auth_objects import DATA_EXPORTER_ROLE
from edc_facility.auth_objects import (
    EDC_FACILITY,
    EDC_FACILITY_SUPER,
    EDC_FACILITY_VIEW,
)
from edc_he.auths import EDC_HEALTH_ECONOMICS_VIEW
from edc_screening.auth_objects import SCREENING, SCREENING_SUPER, SCREENING_VIEW
from edc_subject_dashboard.auths import SUBJECT_VIEW
from edc_unblinding.auth_objects import UNBLINDING_REQUESTORS

from .auth_objects import clinic_codenames, screening_codenames

site_auths.add_pii_model("intecomm_prn.subjectlocator")

# update edc_auth default groups
site_auths.update_group(*clinic_codenames, name=AUDITOR, view_only=True)
site_auths.update_group(*data_manager_codenames, name=AUDITOR, view_only=True)

site_auths.update_group(*clinic_codenames, name=CLINIC, no_delete=True)
site_auths.update_group(*clinic_codenames, name=CLINIC_SUPER)
site_auths.update_group(*screening_codenames, name=SCREENING, no_delete=True)
site_auths.update_group(*screening_codenames, name=SCREENING_SUPER)
site_auths.update_group(*screening_codenames, name=SCREENING_VIEW, view_only=True)

# update edc_auth default roles
site_auths.update_role(
    EDC_HEALTH_ECONOMICS_VIEW,
    EDC_FACILITY_VIEW,
    name=AUDITOR_ROLE,
)
site_auths.update_role(
    UNBLINDING_REQUESTORS,
    EDC_HEALTH_ECONOMICS_VIEW,
    EDC_FACILITY,
    name=CLINICIAN_ROLE,
)
site_auths.update_role(
    UNBLINDING_REQUESTORS,
    EDC_HEALTH_ECONOMICS_VIEW,
    EDC_FACILITY_SUPER,
    name=CLINICIAN_SUPER_ROLE,
)
site_auths.update_role(
    ACTION_ITEM_EXPORT,
    APPOINTMENT_EXPORT,
    DATA_MANAGER_EXPORT,
    name=DATA_EXPORTER_ROLE,
)
site_auths.update_role(SUBJECT_VIEW, SCREENING_VIEW, name=DATA_MANAGER_ROLE)
site_auths.update_role(
    SUBJECT_VIEW, SCREENING_VIEW, ACTION_ITEM, UNBLINDING_REQUESTORS, name=TMG_ROLE
)
