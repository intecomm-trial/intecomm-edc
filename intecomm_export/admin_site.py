from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

intecomm_export_admin = EdcAdminSite(name="intecomm_export_admin", app_label=AppConfig.name)
