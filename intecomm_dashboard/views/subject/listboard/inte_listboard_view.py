import re
from typing import List
from uuid import uuid4

from django.db.models import Q
from edc_listboard.views import SubjectListboardView as BaseSubjectListboardView


class InteSubjectListboardView(BaseSubjectListboardView):

    listboard_template = "inte_subject_listboard_template"
    listboard_url = "inte_subject_listboard_url"
    navbar_selected_item = "inte_followup"
    search_form_url = "inte_subject_listboard_url"

    def get_queryset(self):
        # TODO
        qs = super().get_queryset()
        return qs.filter(id=uuid4())

    def extra_search_options(self, search_term) -> List[Q]:
        q_objects = super().extra_search_options(search_term)
        if re.match(r"^[0-9\-]+$", search_term):
            q_objects.append(Q(identity__exact=search_term))
        return q_objects
