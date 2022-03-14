from django.apps import AppConfig as DjangoApponfig


class AppConfig(DjangoApponfig):
    name = "intecomm_auth"
    verbose_name = "INTECOMM: Authentication and Permissions"
    default_auto_field = "django.db.models.BigAutoField"
