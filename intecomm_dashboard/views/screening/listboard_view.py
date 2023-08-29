import re
from typing import List

from django.apps import apps as django_apps
from django.db.models import Q
from django.urls import reverse
from edc_listboard.filters import ListboardFilter
from edc_listboard.filters import ListboardViewFilters as Base
from edc_listboard.views import ScreeningListboardView
from edc_sites import get_current_country

from intecomm_screening.constants import UGANDA

from ...model_wrappers import SubjectScreeningModelWrapper


class ListboardViewFilters(Base):
    all = ListboardFilter(name="all", label="All", lookup={})

    eligible = ListboardFilter(label="Eligible", position=10, lookup={"eligible": True})

    not_eligible = ListboardFilter(
        label="Not Eligible", position=11, lookup={"eligible": False}
    )

    consented = ListboardFilter(
        label="Consented", position=20, lookup={"eligible": True, "consented": True}
    )

    not_consented = ListboardFilter(
        label="Not consented",
        position=21,
        lookup={"eligible": True, "consented": False},
    )

    grouped = ListboardFilter(
        label="Grouped",
        position=30,
        lookup={
            "patient_log__patientgroup__isnull": False,
            "consented": True,
            "eligible": True,
        },
    )

    not_grouped = ListboardFilter(
        label="Not Grouped",
        position=31,
        lookup={
            "patient_log__patientgroup__isnull": True,
            "consented": True,
            "eligible": True,
        },
    )


class ListboardView(ScreeningListboardView):
    listboard_model = "intecomm_screening.subjectscreening"
    model_wrapper_cls = SubjectScreeningModelWrapper
    navbar_selected_item = "screen_group"
    listboard_view_filters = ListboardViewFilters()
    listboard_panel_title = "Screening"

    @property
    def listboard_model_cls(self):
        if get_current_country(request=self.request) == UGANDA:
            return django_apps.get_model("intecomm_screening.subjectscreeningug")
        return django_apps.get_model(self.listboard_model)

    def get_patient_log_add_url(self):
        if get_current_country(request=self.request) == UGANDA:
            return reverse("intecomm_screening_admin:intecomm_screening_patientlogug_add")
        return reverse("intecomm_screening_admin:intecomm_screening_patientlog_add")

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            patient_log_add_url=self.get_patient_log_add_url(),
        )
        return context_data

    def extra_search_options(self, search_term) -> List[Q]:
        q_objects = super().extra_search_options(search_term)
        if re.match(r"^[0-9\-]+$", search_term):
            q_objects.append(Q(hospital_identifier__exact=search_term))
        return q_objects
