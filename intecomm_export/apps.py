from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "intecomm_export"
    verbose_name = "INTECOMM: Export Data"
