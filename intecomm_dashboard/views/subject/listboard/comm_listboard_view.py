from intecomm_rando.constants import COMM_INTERVENTION

from .base_subject_listboard_view import BaseSubjectListboardView


class CommSubjectListboardView(BaseSubjectListboardView):
    listboard_template = "comm_subject_listboard_template"
    listboard_url = "comm_subject_listboard_url"
    navbar_selected_item = "comm_followup"
    search_form_url = "comm_subject_listboard_url"
    listboard_fa_icon = "fas fa-users-between-lines fa-2x"
    assignment = COMM_INTERVENTION
    followup_url = "followup_comm_url"
