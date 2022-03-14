from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa

SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = False
ALLOWED_HOSTS = [
    "mnazi-moja.tz.intecomm.clinicedc.org",
    "mbagala.tz.intecomm.clinicedc.org",
    "mwananyamala.tz.intecomm.clinicedc.org",
    "hindu-mandal.tz.intecomm.clinicedc.org",
    "temeke.tz.intecomm.clinicedc.org",
    "amana.tz.intecomm.clinicedc.org",
    "localhost",
]
