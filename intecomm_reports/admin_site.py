from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

intecomm_reports_admin = EdcAdminSite(name="intecomm_reports_admin", app_label=AppConfig.name)
