from __future__ import annotations

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import Q
from django.urls import reverse
from edc_listboard.views import SubjectListboardView
from edc_sites.site import sites
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM

from intecomm_group.models import PatientGroup
from intecomm_group.utils import get_assignment_for_patient_group


class BaseSubjectListboardView(SubjectListboardView):
    listboard_model = "intecomm_screening.patientlog"
    assignment: str = None
    followup_url: str = None
    show_change_form_button: bool = False

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
            followup_url=reverse(self.followup_url),
            patient_group_url=self.get_patient_group_url(**kwargs),
            patient_group_appointment_url=self.get_patient_group_appointment_url(**kwargs),
            patient_group_meeting_url=self.get_patient_group_meeting_url(**kwargs),
            patient_group=self.patient_group,
            arm=self.arm,
            COMMUNITY_ARM=COMMUNITY_ARM,
            FACILITY_ARM=FACILITY_ARM,
            site=getattr(self.request, "site", None),
            country=sites.get_current_country(self.request),
        )
        return super().get_context_data(**kwargs)

    def get_queryset_filter_options(self, request, *args, **kwargs) -> tuple[Q, dict]:
        q_options, options = super().get_queryset_filter_options(request, *args, **kwargs)
        options.update(subject_identifier__startswith="107-", group_identifier__isnull=False)
        return q_options, options

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
