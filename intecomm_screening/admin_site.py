from __future__ import annotations

from edc_model_admin.admin_site import EdcAdminSite
from edc_sites.site import sites
from intecomm_rando.constants import UGANDA

from .apps import AppConfig
from .intecomm_admin_site_mixin import IntecommAdminSiteMixin


class IntecommScreeningSite(IntecommAdminSiteMixin, EdcAdminSite):
    @staticmethod
    def get_hidden_models(request) -> dict:
        if sites.get_current_country(request) == UGANDA:
            hidden_models = {
                "intecomm_screening": ["PatientLog", "SubjectScreening"],
            }
        else:
            hidden_models = {
                "intecomm_screening": ["PatientLogUg", "SubjectScreeningUg"],
            }
        return hidden_models


intecomm_screening_admin = IntecommScreeningSite(
    name="intecomm_screening_admin", app_label=AppConfig.name
)
