from django.views.generic import TemplateView


class ToGroupView(TemplateView):
    template_name = None

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        return context_data
