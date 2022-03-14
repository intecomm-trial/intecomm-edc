from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "intecomm_consent"
    verbose_name = "INTECOMM: Consent"
    include_in_administration_section = True
    has_exportable_data = True
    default_auto_field = "django.db.models.BigAutoField"
