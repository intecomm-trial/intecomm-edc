import os  # noqa

from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")

# UG
# SITE_ID = SiteID(default=101)  # Kasangati
# SITE_ID = SiteID(default=102)  # Kisugu
# SITE_ID = SiteID(default=103)  # Kiswa
# SITE_ID = SiteID(default=104)  # Kyazanga
# SITE_ID = SiteID(default=105)  # Mpigi
# SITE_ID = SiteID(default=106)  # Namayumba
# SITE_ID = SiteID(default=107)  # Namulonge
SITE_ID = SiteID(default=108)  # Ndejje
# SITE_ID = SiteID(default=109)  # Sekiwunga
# SITE_ID = SiteID(default=110)  # Wakiso

# TZ
# SITE_ID = SiteID(default=201)  # Amana
# SITE_ID = SiteID(default=202)  # Bagamoyo
# SITE_ID = SiteID(default=203)  # Rugambwa
# SITE_ID = SiteID(default=204)  # Hindu_Mandal
# SITE_ID = SiteID(default=205)  # Kisarawe
# SITE_ID = SiteID(default=206)  # Mbagala
# SITE_ID = SiteID(default=207)  # Mnazi_Moja
# SITE_ID = SiteID(default=208)  # Mwananyamala
# SITE_ID = SiteID(default=209)  # Sinza
# SITE_ID = SiteID(default=210)  # Temeke

EDC_SITES_UAT_DOMAIN = False
DEBUG = True
ALLOWED_HOSTS = [
    "localhost",
]

SECURE_SSL_REDIRECT = False
EDC_MODEL_ADMIN_CSS_THEME = "edc_purple"

if os.path.exists(BASE_DIR) and not os.path.exists(KEY_PATH):  # noqa
    os.makedirs(KEY_PATH)  # noqa
    AUTO_CREATE_KEYS = True
