from django.apps import AppConfig as DjangoAppConfig
from django.contrib.admin.apps import AdminConfig as DjangoAdminConfig
from django.core.management.color import color_style

style = color_style()


class AdminConfig(DjangoAdminConfig):
    default_site = "intecomm_edc.admin.AdminSite"


class AppConfig(DjangoAppConfig):
    name = "intecomm_edc"
    verbose_name = "INTECOMM"
