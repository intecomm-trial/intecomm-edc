from django.urls import reverse
from edc_subject_dashboard.views import SubjectDashboardView

from intecomm_group.models import PatientGroup


class DashboardView(SubjectDashboardView):
    consent_model = "intecomm_consent.subjectconsent"
    navbar_selected_item = "consented_subject"
    visit_model = "intecomm_subject.subjectvisit"
    history_button_label = "Audit"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = PatientGroup.objects.get(
            group_identifier=context.get("consent").object.group_identifier
        )
        url = reverse("intecomm_group_admin:intecomm_group_patientgroup_changelist")
        url = f"{url}?q={group.name}"

        context.update(
            subject_listboard_url="screen_group_url",
            group_identifier=group.group_identifier,
            group_name=group.name,
            patient_group_url=url,
        )
        return context
