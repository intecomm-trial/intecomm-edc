from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "intecomm_labs"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "INTECOMM: Labs"
