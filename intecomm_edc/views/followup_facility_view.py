from typing import Any

from django.conf import settings
from django.views.generic import TemplateView
from edc_dashboard.view_mixins import EdcViewMixin
from edc_navbar import NavbarViewMixin


class FollowupFacilityView(EdcViewMixin, NavbarViewMixin, TemplateView):
    template_name = f"intecomm_edc/bootstrap{settings.EDC_BOOTSTRAP}/followup_facility.html"
    navbar_name = settings.APP_NAME
    navbar_selected_item = "facility_followup"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        kwargs.update(
            facility_subject_listboard_url="intecomm_dashboard:facility_subject_listboard_url"
        )
        return super().get_context_data(**kwargs)
