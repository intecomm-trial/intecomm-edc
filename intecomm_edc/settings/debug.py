import os  # noqa

from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa

SITE_ID = SiteID(default=201)
EDC_SITES_UAT_DOMAIN = False
DEBUG = True
ALLOWED_HOSTS = [
    "localhost",
    "amana.uat.tz.intecomm.clinicedc.org",
    "bagamoyo.uat.tz.intecomm.clinicedc.org",
    "hindu-mandal.uat.tz.intecomm.clinicedc.org",
    "kasangati.uat.ug.intecomm.clinicedc.org",
    "kisarawe.uat.tz.intecomm.clinicedc.org",
    "kisugu.uat.ug.intecomm.clinicedc.org",
    "kiswa.uat.ug.intecomm.clinicedc.org",
    "kyazanga.uat.ug.intecomm.clinicedc.org",
    "mbagala.uat.tz.intecomm.clinicedc.org",
    "mnazi.uat.tz.intecomm.clinicedc.org",
    "mpigi.uat.ug.intecomm.clinicedc.org",
    "mwananyamala.uat.tz.intecomm.clinicedc.org",
    "namayumba.uat.ug.intecomm.clinicedc.org",
    "namulonge.uat.ug.intecomm.clinicedc.org",
    "ndejje.uat.ug.intecomm.clinicedc.org",
    "rugambwa.uat.tz.intecomm.clinicedc.org",
    "sekiwunga.uat.ug.intecomm.clinicedc.org",
    "sinza.uat.tz.intecomm.clinicedc.org",
    "temeke.uat.tz.intecomm.clinicedc.org",
    "wakiso.uat.ug.intecomm.clinicedc.org",
]

SECURE_SSL_REDIRECT = False

if os.path.exists(BASE_DIR) and not os.path.exists(KEY_PATH):  # noqa
    os.makedirs(KEY_PATH)  # noqa
    AUTO_CREATE_KEYS = True
