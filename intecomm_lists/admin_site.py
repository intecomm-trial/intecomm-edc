from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

intecomm_lists_admin = EdcAdminSite(name="intecomm_lists_admin", app_label=AppConfig.name)
