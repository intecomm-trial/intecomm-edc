from typing import Any

from django.conf import settings
from django.views.generic import TemplateView
from edc_dashboard.view_mixins import EdcViewMixin
from edc_navbar import NavbarViewMixin


class SubjectsHomeView(EdcViewMixin, NavbarViewMixin, TemplateView):
    template_name = "intecomm_edc/subjects_home.html"
    navbar_name = settings.APP_NAME
    navbar_selected_item = "subjects"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        kwargs.update(subject_listboard_url="intecomm_dashboard:subject_listboard_url")
        return super().get_context_data(**kwargs)
