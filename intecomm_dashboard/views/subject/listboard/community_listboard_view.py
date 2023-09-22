from intecomm_rando.constants import COMMUNITY_ARM

from .base_subject_listboard_view import BaseSubjectListboardView


class CommunitySubjectListboardView(BaseSubjectListboardView):
    listboard_template = "community_subject_listboard_template"
    listboard_url = "community_subject_listboard_url"
    navbar_selected_item = "comm_followup"
    search_form_url = "community_subject_listboard_url"
    listboard_fa_icon = "fas fa-users-between-lines fa-2x"
    assignment = COMMUNITY_ARM
    followup_url = "followup_community_url"
    listboard_panel_title = "Community group participants"
