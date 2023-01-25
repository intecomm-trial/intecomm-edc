import re
from typing import List

from django.db.models import Q
from edc_listboard.views import SubjectListboardView as BaseSubjectListboardView

from ....model_wrappers import SubjectConsentModelWrapper


class CommSubjectListboardView(BaseSubjectListboardView):

    listboard_template = "comm_subject_listboard_template"
    listboard_url = "comm_subject_listboard_url"
    navbar_selected_item = "comm_followup"
    search_form_url = "comm_subject_listboard_url"
    listboard_fa_icon = "fas fa-users-between-lines fa-2x"
    model_wrapper_cls = SubjectConsentModelWrapper
    name_search_field: str = "legal_name"
    identity_regex: str = r"^[A-Z0-9\ ]+$"

    def get_queryset(self):
        # TODO: expand filter??
        qs = super().get_queryset()
        return qs.filter(group_identifier__isnull=False)

    def extra_search_options(self, search_term) -> List[Q]:
        q_objects = super().extra_search_options(search_term)
        if re.match(r"^[A-Za-z\-]+$", search_term):
            q_objects.append(Q(familiar_name__exact=search_term))
        if re.match(r"^[0-9\-]+$", search_term):
            q_objects.append(Q(group_identifier__exact=search_term))
        return q_objects
