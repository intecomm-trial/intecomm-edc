from django_audit_fields import ModelAdminAuditFieldsMixin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_model_admin.mixins import (
    ModelAdminFormAutoNumberMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminGetFormClsMixin,
    ModelAdminInstitutionMixin,
    ModelAdminNextUrlRedirectMixin,
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
