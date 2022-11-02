from importlib.metadata import version

from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")
print(f"Version: {version('intecomm_edc')}")

SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = True
EDC_CONSENT_BYPASS_CONSENT_DATETIME_VALIDATION = True
ALLOWED_HOSTS = [
    "kasangati.uat.ug.intecomm.clinicedc.org",
    "kisugu.uat.ug.intecomm.clinicedc.org",
    "kiswa.uat.ug.intecomm.clinicedc.org",
    "kyazanga.uat.ug.intecomm.clinicedc.org",
    "mpigi.uat.ug.intecomm.clinicedc.org",
    "namayumba.uat.ug.intecomm.clinicedc.org",
    "namulonge.uat.ug.intecomm.clinicedc.org",
    "ndejje.uat.ug.intecomm.clinicedc.org",
    "sekiwunga.uat.ug.intecomm.clinicedc.org",
    "wakiso.uat.ug.intecomm.clinicedc.org",
    "amana.uat.tz.intecomm.clinicedc.org",
    "bagamoyo.uat.tz.intecomm.clinicedc.org",
    "rugambwa.uat.tz.intecomm.clinicedc.org",
    "hindu-mandal.uat.tz.intecomm.clinicedc.org",
    "kisarawe.uat.tz.intecomm.clinicedc.org",
    "mbagala.uat.tz.intecomm.clinicedc.org",
    "mnazi.uat.tz.intecomm.clinicedc.org",
    "mwananyamala.uat.tz.intecomm.clinicedc.org",
    "sinza.uat.tz.intecomm.clinicedc.org",
    "temeke.uat.tz.intecomm.clinicedc.org",
]

# edc_model_admin
EDC_MODEL_ADMIN_CSS_THEME = "edc_purple"
LIVE_SYSTEM = False
