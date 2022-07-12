from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa

SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = False
ALLOWED_HOSTS = [
    "amana.tz.intecomm.clinicedc.org",
    "bagamoyo.tz.intecomm.clinicedc.org",
    "hindu-mandal.tz.intecomm.clinicedc.org",
    "kasangati.ug.intecomm.clinicedc.org",
    "kisarawe.tz.intecomm.clinicedc.org",
    "kisugu.ug.intecomm.clinicedc.org",
    "kiswa.ug.intecomm.clinicedc.org",
    "kyazanga.ug.intecomm.clinicedc.org",
    "mbagala.tz.intecomm.clinicedc.org",
    "mnazi.tz.intecomm.clinicedc.org",
    "mpigi.ug.intecomm.clinicedc.org",
    "mwananyamala.tz.intecomm.clinicedc.org",
    "namayumba.ug.intecomm.clinicedc.org",
    "namulonge.ug.intecomm.clinicedc.org",
    "ndejje.ug.intecomm.clinicedc.org",
    "rugambwa.tz.intecomm.clinicedc.org",
    "sekiwunga.ug.intecomm.clinicedc.org",
    "sinza.tz.intecomm.clinicedc.org",
    "temeke.tz.intecomm.clinicedc.org",
    "wakiso.ug.intecomm.clinicedc.org",
    "localhost",
]
