import sys

from django.apps import AppConfig as DjangoAppConfig
from django.apps import apps as django_apps
from django.core.management.color import color_style
from django.db.models.signals import post_migrate

style = color_style()


def post_migrate_update_sites(sender=None, **kwargs):
    from edc_sites.utils import add_or_update_django_sites

    sys.stdout.write(style.MIGRATE_HEADING("Updating sites:\n"))
    add_or_update_django_sites(apps=django_apps, verbose=True)
    sys.stdout.write("Done.\n")
    sys.stdout.flush()


class AppConfig(DjangoAppConfig):
    name = "intecomm_sites"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "INTECOMM: Sites"

    def ready(self):
        post_migrate.connect(post_migrate_update_sites, sender=self)
