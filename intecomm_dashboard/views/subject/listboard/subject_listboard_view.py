import re
from typing import List

from django.db.models import Q
from edc_listboard.views import SubjectListboardView as BaseSubjectListboardView


class SubjectListboardView(BaseSubjectListboardView):

    listboard_template = "subject_listboard_template"
    listboard_url = "subject_listboard_url"
    navbar_selected_item = "baseline"
    search_form_url = "subject_listboard_url"
    listboard_fa_icon = "fas fa-users-between-lines fa-2x"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def extra_search_options(self, search_term) -> List[Q]:
        q_objects = super().extra_search_options(search_term)
        if re.match(r"^[0-9\-]+$", search_term):
            q_objects.append(Q(identity__exact=search_term))
        return q_objects
