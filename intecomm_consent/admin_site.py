from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

intecomm_consent_admin = EdcAdminSite(name="intecomm_consent_admin", app_label=AppConfig.name)
