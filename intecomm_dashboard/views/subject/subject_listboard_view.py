from __future__ import annotations

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import Q
from django.urls import reverse
from edc_dashboard.view_mixins import EdcViewMixin
from edc_listboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_listboard.views import ListboardView as BaseListboardView
from edc_navbar import NavbarViewMixin
from edc_protocol.research_protocol_config import ResearchProtocolConfig
from edc_sites import site_sites

from intecomm_group.models import PatientGroup
from intecomm_group.utils import get_assignment_for_patient_group


class SubjectListboardView(
    EdcViewMixin,
    NavbarViewMixin,
    ListboardFilterViewMixin,
    SearchFormViewMixin,
    BaseListboardView,
):
    listboard_template = "subject_listboard_template"
    listboard_url = "subject_listboard_url"
    listboard_panel_style = "success"
    listboard_panel_title = "Subjects in randomized groups"
    listboard_fa_icon = "far fa-user-circle"
    listboard_model = "intecomm_screening.patientlog"
    listboard_view_permission_codename = "edc_subject_dashboard.view_subject_listboard"
    navbar_selected_item = "subjects"
    search_form_url = "subject_listboard_url"
    ordering: str = "-subject_identifier"
    show_change_form_button = False
    paginate_by = 20
    search_fields = [
        "user_created",
        "user_modified",
        "screening_identifier",
        "subject_identifier",
        "group_identifier",
        "patient_log_identifier",
        "filing_identifier",
        "initials__exact",
        "hospital_identifier__exact",
        "last_4_hospital_identifier",
        "contact_number__exact",
        "alt_contact_number__exact",
        "last_4_contact_number",
        "legal_name__exact",
    ]

    def get_context_data(self, **kwargs) -> dict:
        kwargs.update(
            patient_group_url=self.get_patient_group_url(**kwargs),
            patient_group_appointment_url=self.get_patient_group_appointment_url(**kwargs),
            patient_group_meeting_url=self.get_patient_group_meeting_url(**kwargs),
            patient_group=self.patient_group,
            # arm=self.arm,
            site=getattr(self.request, "site", None),
            country=site_sites.get_current_country(self.request),
        )
        return super().get_context_data(**kwargs)

    def get_queryset_filter_options(self, request, *args, **kwargs) -> tuple[Q, dict]:
        number = ResearchProtocolConfig().protocol_number
        q_object, options = super().get_queryset_filter_options(request, *args, **kwargs)
        options.update(
            subject_identifier__startswith=f"{number}-", group_identifier__isnull=False
        )
        if kwargs.get("subject_identifier"):
            options.update({"subject_identifier": kwargs.get("subject_identifier")})
        return q_object, options

    @property
    def patient_group(self) -> PatientGroup:
        try:
            obj = PatientGroup.objects.get(
                Q(group_identifier__exact=self.raw_search_term)
                | Q(name__exact=self.raw_search_term)
            )
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            obj = None
        return obj

    def get_patient_group_url(self, **kwargs) -> str:
        url = reverse("intecomm_group_admin:intecomm_group_patientgroup_changelist")
        return f"{url}?q={self.raw_search_term}"

    def get_patient_group_appointment_url(self, **kwargs) -> str:
        url = reverse("intecomm_group_admin:intecomm_group_patientgroupappointment_changelist")
        return f"{url}?q={self.raw_search_term}"

    def get_patient_group_meeting_url(self, **kwargs) -> str:
        url = reverse("intecomm_group_admin:intecomm_group_patientgroupmeeting_changelist")
        return f"{url}?q={self.raw_search_term}"

    @property
    def arm(self) -> str | None:
        if self.patient_group:
            return get_assignment_for_patient_group(self.patient_group.group_identifier)
        return None
