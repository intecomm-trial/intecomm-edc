from intecomm_rando.constants import FACILITY_ARM

from .base_subject_listboard_view import BaseSubjectListboardView


class FacilitySubjectListboardView(BaseSubjectListboardView):
    listboard_template = "facility_subject_listboard_template"
    listboard_url = "facility_subject_listboard_url"
    navbar_selected_item = "inte_followup"
    search_form_url = "facility_subject_listboard_url"
    assignment = FACILITY_ARM
    followup_url = "followup_facility_url"
    listboard_panel_title = "Facility-based participants"
