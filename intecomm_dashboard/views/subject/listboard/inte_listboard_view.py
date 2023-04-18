from intecomm_rando.constants import CLINIC_CONTROL

from .base_subject_listboard_view import BaseSubjectListboardView


class InteSubjectListboardView(BaseSubjectListboardView):
    listboard_template = "inte_subject_listboard_template"
    listboard_url = "inte_subject_listboard_url"
    navbar_selected_item = "inte_followup"
    search_form_url = "inte_subject_listboard_url"
    assignment = CLINIC_CONTROL
    followup_url = "followup_inte_url"
