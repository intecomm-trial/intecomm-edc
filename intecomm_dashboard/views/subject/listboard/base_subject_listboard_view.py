import re
from typing import List

from django.db.models import Q
from django.urls import reverse
from edc_listboard.views import SubjectListboardView
from intecomm_rando.models import RandomizationList

from ....model_wrappers import SubjectConsentModelWrapper


class BaseSubjectListboardView(SubjectListboardView):
    model_wrapper_cls = SubjectConsentModelWrapper
    name_search_field: str = "legal_name"
    identity_regex: str = r"^[A-Z0-9\ ]+$"
    assignment: str = None
    followup_url: str = None

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update(followup_url=reverse(self.followup_url))
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        values_list = RandomizationList.objects.values_list("group_identifier").filter(
            group_identifier__isnull=False, assignment=self.assignment
        )
        return qs.filter(group_identifier__in=values_list)

    def extra_search_options(self, search_term) -> List[Q]:
        q_objects = super().extra_search_options(search_term)
        if re.match(r"^[A-Za-z\-]+$", search_term):
            q_objects.append(Q(familiar_name__exact=search_term))
        if re.match(r"^[0-9\-]+$", search_term):
            q_objects.append(Q(group_identifier__exact=search_term))
        return q_objects
