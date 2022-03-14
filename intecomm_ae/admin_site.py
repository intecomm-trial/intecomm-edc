from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

intecomm_ae_admin = EdcAdminSite(name="intecomm_ae_admin", app_label=AppConfig.name)
