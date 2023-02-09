from django.conf import settings
from django.views.generic import TemplateView
from edc_dashboard.view_mixins import EdcViewMixin
from edc_navbar import NavbarViewMixin


class FollowupInteView(EdcViewMixin, NavbarViewMixin, TemplateView):
    template_name = f"intecomm_edc/bootstrap{settings.EDC_BOOTSTRAP}/followup_inte.html"
    navbar_name = settings.APP_NAME
    navbar_selected_item = "inte_followup"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            inte_subject_listboard_url="intecomm_dashboard:inte_subject_listboard_url"
        )
        return context
