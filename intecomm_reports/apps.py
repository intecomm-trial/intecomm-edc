from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "intecomm_reports"
    verbose_name = "INTECOMM Reports"
    include_in_administration_section = True
