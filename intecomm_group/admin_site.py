from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

intecomm_group_admin = EdcAdminSite(name="intecomm_group_admin", app_label=AppConfig.name)
