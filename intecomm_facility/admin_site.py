from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

intecomm_facility_admin = EdcAdminSite(
    name="intecomm_facility_admin", app_label=AppConfig.name
)
