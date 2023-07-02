from __future__ import annotations

from django.urls import reverse
from django_audit_fields import ModelAdminAuditFieldsMixin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_model_admin.mixins import (
    ModelAdminFormAutoNumberMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminGetFormClsMixin,
    ModelAdminInstitutionMixin,
    ModelAdminNextUrlRedirectMixin,
    ModelAdminRedirectAllToChangelistMixin,
    TemplatesModelAdminMixin,
)
from edc_sites.modeladmin_mixins import SiteModelAdminMixin


class BaseModelAdminMixin(
    TemplatesModelAdminMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin,
    ModelAdminRevisionMixin,
    ModelAdminInstitutionMixin,
    ModelAdminNextUrlRedirectMixin,
    ModelAdminAuditFieldsMixin,
    SiteModelAdminMixin,
    ModelAdminGetFormClsMixin,
    SimpleHistoryAdmin,
):
    show_cancel = True
    view_on_site = False
    save_on_top = True


class RedirectAllToPatientLogModelAdminMixin(ModelAdminRedirectAllToChangelistMixin):
    changelist_url = "intecomm_screening_admin:intecomm_screening_patientlog_changelist"
    search_field_name = "screening_identifier"


class ChangeListTopBarModelAdminMixin:
    changelist_top_bar_selected: str = None
    changelist_top_bar_add_url: str = None

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["changelist_top_bar_selected"] = self.changelist_top_bar_selected
        extra_context["changelist_top_bar_add_url"] = reverse(self.changelist_top_bar_add_url)
        return super().changelist_view(request, extra_context=extra_context)
