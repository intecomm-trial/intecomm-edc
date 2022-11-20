import re
from typing import List

from django.db.models import Q
from django.urls import reverse
from edc_listboard.views import ScreeningListboardView
from edc_screening.model_wrappers import SubjectScreeningModelWrapper


class ListboardView(ScreeningListboardView):

    listboard_model = "intecomm_screening.subjectscreening"
    model_wrapper_cls = SubjectScreeningModelWrapper
    navbar_selected_item = "screen_group"

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        patient_log_add_url = reverse(
            "intecomm_screening_admin:intecomm_screening_patientlog_add"
        )
        context_data.update(patient_log_add_url=patient_log_add_url)
        return context_data

    def extra_search_options(self, search_term) -> List[Q]:
        q_objects = super().extra_search_options(search_term)
        if re.match(r"^[0-9\-]+$", search_term):
            q_objects.append(Q(hospital_identifier__exact=search_term))
        return q_objects
