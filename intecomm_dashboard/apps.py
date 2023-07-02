from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "intecomm_dashboard"
    verbose_name = "INTECOMM: Dashboard"
    admin_site_name = "meta_test_admin"
    include_in_administration_section = False
