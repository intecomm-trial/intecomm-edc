from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

intecomm_screening_admin = EdcAdminSite(
    name="intecomm_screening_admin", app_label=AppConfig.name
)
