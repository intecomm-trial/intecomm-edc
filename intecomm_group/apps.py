from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "intecomm_group"
    verbose_name = "INTECOMM: Group Forms"
    include_in_administration_section = True
    has_exportable_data = True
    default_auto_field = "django.db.models.BigAutoField"
