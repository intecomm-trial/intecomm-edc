import re
from typing import List

from django.db.models import Q
from edc_listboard.views import ScreeningListboardView
from edc_screening.model_wrappers import SubjectScreeningModelWrapper


class ListboardView(ScreeningListboardView):

    listboard_model = "intecomm_screening.subjectscreening"
    model_wrapper_cls = SubjectScreeningModelWrapper
    navbar_selected_item = "screened_subject"

    def extra_search_options(self, search_term) -> List[Q]:
        q_objects = super().extra_search_options(search_term)
        if re.match(r"^[0-9\-]+$", search_term):
            q_objects.append(Q(hospital_identifier__exact=search_term))
        return q_objects
