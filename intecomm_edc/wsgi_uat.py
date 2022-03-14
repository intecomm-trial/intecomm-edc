import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intecomm_edc.settings.uat")

application = get_wsgi_application()
