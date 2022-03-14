from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa

SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = True
EDC_CONSENT_BYPASS_CONSENT_DATETIME_VALIDATION = True
ALLOWED_HOSTS = [
    "mnazi-moja.uat.tz.intecomm.clinicedc.org",
    "mbagala.uat.tz.intecomm.clinicedc.org",
    "mwananyamala.uat.tz.intecomm.clinicedc.org",
    "hindu-mandal.uat.tz.intecomm.clinicedc.org",
    "temeke.uat.tz.intecomm.clinicedc.org",
    "amana.uat.tz.intecomm.clinicedc.org",
    "localhost",
]
