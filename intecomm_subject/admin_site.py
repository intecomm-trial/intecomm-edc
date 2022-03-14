from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

intecomm_subject_admin = EdcAdminSite(name="intecomm_subject_admin", app_label=AppConfig.name)
