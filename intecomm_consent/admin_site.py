from __future__ import annotations

from edc_model_admin.admin_site import EdcAdminSite
from edc_sites import get_current_country

from intecomm_screening.constants import UGANDA
from intecomm_screening.intecomm_admin_site_mixin import IntecommAdminSiteMixin

from .apps import AppConfig


class IntecommConsentSite(IntecommAdminSiteMixin, EdcAdminSite):
    @staticmethod
    def get_hidden_models(request) -> dict:
        if get_current_country(request=request) == UGANDA:
            hidden_models = {"intecomm_consent": ["SubjectConsent"]}
        else:
            hidden_models = {"intecomm_consent": ["SubjectConsentUg"]}
        return hidden_models


intecomm_consent_admin = IntecommConsentSite(
    name="intecomm_consent_admin", app_label=AppConfig.name
)
