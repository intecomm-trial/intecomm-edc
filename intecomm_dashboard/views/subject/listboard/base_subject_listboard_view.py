from __future__ import annotations

import re
from typing import List

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import Q
from django.urls import reverse
from edc_listboard.views import SubjectListboardView
from edc_sites import get_current_country
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM
from intecomm_rando.models import RandomizationList

from intecomm_group.models import PatientGroup
from intecomm_group.utils import get_assignment_for_patient_group
from intecomm_screening.models import PatientLog

from ....model_wrappers import PatientLogModelWrapper as BaseModelWrapper


class PatientLogModelWrapper(BaseModelWrapper):
    model = "intecomm_screening.patientlog"
    next_url_attrs = ["subject_identifier"]
    next_url_name = "subject_dashboard_url"


class BaseSubjectListboardView(SubjectListboardView):
    listboard_model = PatientLog
    model_wrapper_cls = PatientLogModelWrapper
    search_fields = [
        "group_identifier",
        "patientgroup__name",
        "subject_identifier",
        "screening_identifier",
        "initials",
        "filing_identifier",
        "contact_number",
        "patient_log_identifier",
        "last_4_hospital_identifier",
        "last_4_contact_number",
    ]
    name_search_field: str = "legal_name"
    identity_regex: str = r"^[A-Z0-9\ ]+$"
    identity_fields = ["hospital_identifier"]
    assignment: str = None
    followup_url: str = None

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update(
            followup_url=reverse(self.followup_url),
            patient_group_url=self.get_patient_group_url(**kwargs),
            patient_group_appointment_url=self.get_patient_group_appointment_url(**kwargs),
            patient_group_meeting_url=self.get_patient_group_meeting_url(**kwargs),
            patient_group=self.patient_group,
            arm=self.arm,
            COMMUNITY_ARM=COMMUNITY_ARM,
            FACILITY_ARM=FACILITY_ARM,
        )
        context.update(
            site=getattr(self.request, "site", None),
            country=get_current_country(request=self.request),
        )
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        values_list = RandomizationList.objects.values_list("group_identifier").filter(
            group_identifier__isnull=False, assignment=self.assignment
        )
        return qs.filter(group_identifier__in=values_list)

    def extra_search_options(self, search_term) -> List[Q]:
        q_objects = super().extra_search_options(search_term)
        if re.match(r"^[A-Za-z\-]+$", search_term):
            q_objects.append(
                Q(familiar_name__exact=search_term)
                | Q(patientgroup__name__icontains=search_term)
            )
        if re.match(r"^[0-9\-]+$", search_term):
            q_objects.append(Q(group_identifier__exact=search_term))
        return q_objects

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
