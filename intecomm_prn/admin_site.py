from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

intecomm_prn_admin = EdcAdminSite(name="intecomm_prn_admin", app_label=AppConfig.name)
