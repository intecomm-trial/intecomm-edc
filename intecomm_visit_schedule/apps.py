from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "intecomm_visit_schedule"
    verbose_name = "INTECOMM: Visit Schedule"
