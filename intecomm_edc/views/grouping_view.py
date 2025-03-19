from django.conf import settings
from django.views.generic import TemplateView
from edc_dashboard.view_mixins import EdcViewMixin
from edc_navbar import NavbarViewMixin


class GroupingView(EdcViewMixin, NavbarViewMixin, TemplateView):
    template_name = "intecomm_edc/grouping.html"
    navbar_name = settings.APP_NAME
    navbar_selected_item = "screen_group"
