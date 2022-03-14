import os  # noqa

from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa

SITE_ID = SiteID(default=30)
EDC_SITES_UAT_DOMAIN = False
DEBUG = True
ALLOWED_HOSTS = [
    "localhost",
    "mnazi-moja.tz.intecomm.clinicedc.org",
    "mbagala.tz.intecomm.clinicedc.org",
    "mwananyamala.tz.intecomm.clinicedc.org",
    "hindu-mandal.tz.intecomm.clinicedc.org",
    "temeke.tz.intecomm.clinicedc.org",
    "amana.tz.intecomm.clinicedc.org",
]

SECURE_SSL_REDIRECT = False

if os.path.exists(BASE_DIR) and not os.path.exists(KEY_PATH):  # noqa
    os.makedirs(KEY_PATH)  # noqa
    AUTO_CREATE_KEYS = True
