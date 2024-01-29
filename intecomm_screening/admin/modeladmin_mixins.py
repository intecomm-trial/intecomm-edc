from __future__ import annotations

import re
from typing import TYPE_CHECKING

from django.urls import reverse
from django_audit_fields import ModelAdminAuditFieldsMixin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_consent.utils import get_remove_patient_names_from_countries
from edc_constants.constants import UUID_PATTERN
from edc_model_admin.history import SimpleHistoryAdmin
from edc_model_admin.mixins import (
    ModelAdminFormAutoNumberMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminInstitutionMixin,
    ModelAdminNextUrlRedirectMixin,
    ModelAdminRedirectAllToChangelistMixin,
    ModelAdminRedirectOnDeleteMixin,
    TemplatesModelAdminMixin,
)
from edc_notification.modeladmin_mixins import NotificationModelAdminMixin
from edc_sites.site import sites
from intecomm_rando.constants import UGANDA

if TYPE_CHECKING:
    from ..models import PatientLog, SubjectScreening


class BaseModelAdminMixin(
    TemplatesModelAdminMixin,
    ModelAdminRedirectOnDeleteMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin,
    ModelAdminRevisionMixin,
    ModelAdminInstitutionMixin,
    ModelAdminNextUrlRedirectMixin,
    NotificationModelAdminMixin,
    ModelAdminAuditFieldsMixin,
    SimpleHistoryAdmin,
):
    show_cancel = True
    view_on_site = False
    save_on_top = True


class RedirectAllToPatientLogModelAdminMixin(ModelAdminRedirectAllToChangelistMixin):
    change_search_field_name = "screening_identifier"
    add_search_field_name = "screening_identifier"

    def get_changelist_url(self, request):
        if sites.get_current_country(request) == UGANDA:
            return "intecomm_screening_admin:intecomm_screening_patientlogug_changelist"
        return "intecomm_screening_admin:intecomm_screening_patientlog_changelist"


class ChangeListTopBarModelAdminMixin:
    changelist_top_bar_selected: str = None
    changelist_top_bar_add_url: str = None

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["changelist_top_bar_selected"] = self.changelist_top_bar_selected
        extra_context["changelist_top_bar_add_url"] = reverse(self.changelist_top_bar_add_url)
        return super().changelist_view(request, extra_context=extra_context)


class InitialDataModelAdminMixin:
    def initial_form_data(self, request, obj: PatientLog | SubjectScreening) -> dict:
        """Return a dict of initial data that may or may not
        include legal and familiar name.

        Initial is carried over from the previous model. For example:
          * PatientLog data -> SubjectScreening;
          * SubjectScreening -> SubjectConsent
        """
        dct = dict(
            initials=obj.initials,
            hospital_identifier=obj.hospital_identifier,
            site=obj.site.id,
            gender=obj.gender,
            age_in_years=obj.age_in_years,
        )
        if self.include_names(request):
            legal_name = obj.legal_name
            if re.match(UUID_PATTERN, obj.legal_name):
                legal_name = None
            familiar_name = obj.familiar_name
            if re.match(UUID_PATTERN, obj.familiar_name):
                familiar_name = None
            dct.update(
                legal_name=legal_name,
                familiar_name=familiar_name,
            )
        return dct

    @staticmethod
    def include_names(request) -> bool:
        """Return True if legal and familiar name may be included"""
        include_names = True
        for country in get_remove_patient_names_from_countries():
            if request.site.id in [
                s.site_id for s in sites.get_by_country(country, aslist=True)
            ]:
                include_names = False
                break
        return include_names
