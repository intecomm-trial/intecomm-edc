from django import forms
from django.db.models import BLANK_CHOICE_DASH
from django.views.generic import TemplateView
from edc_constants.constants import NEW
from edc_dashboard.view_mixins import EdcViewMixin
from edc_navbar import NavbarViewMixin
from intecomm_form_validators import RECRUITING

from intecomm_screening.constants import NEW_GROUP_CHOICE
from intecomm_screening.models import PatientGroup, PatientLog


def get_patient_group_choices():
    return (
        ((None, BLANK_CHOICE_DASH),)
        + ((NEW, NEW_GROUP_CHOICE),)
        + tuple(
            (o.id, o.name)
            for o in PatientGroup.objects.filter(status__in=[NEW, RECRUITING]).order_by("name")
        )
    )


class GroupAddForm(forms.Form):
    patient_group = forms.ChoiceField(choices=get_patient_group_choices)


class GroupManagementView(EdcViewMixin, NavbarViewMixin, TemplateView):
    template_name = "intecomm_screening/group_management.html"
    navbar_selected_item = "home"
    navbar_name = "default"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data.update(patient_logs=self.fetch_patient_logs(kwargs.get("ids")))
        context_data.update(groups=PatientGroup.objects.filter(status__in=[NEW, RECRUITING]))
        context_data.update(add_form=GroupAddForm())
        return context_data

    def fetch_patient_logs(self, selected_pks: str):
        patient_logs = []
        for pk in selected_pks.split(","):
            patient_logs.append(PatientLog.objects.get(pk=pk))
        return patient_logs


class PrintPatientLogReportView(EdcViewMixin, NavbarViewMixin, TemplateView):
    template_name = "intecomm_screening/group_management.html"
    navbar_selected_item = "home"
    navbar_name = "default"
