import os
import sys
from importlib.metadata import version
from pathlib import Path

import django.conf.locale
import environ
from edc_constants.constants import COMPLETE
from edc_constants.internationalization import EXTRA_LANG_INFO
from edc_protocol_incident.constants import PROTOCOL_INCIDENT
from edc_utils import get_datetime_from_env

env = environ.Env(
    AWS_ENABLED=(bool, False),
    CDN_ENABLED=(bool, False),
    CELERY_ENABLED=(bool, False),
    DATABASE_SQLITE_ENABLED=(bool, False),
    DJANGO_AUTO_CREATE_KEYS=(bool, False),
    DJANGO_CRYPTO_FIELDS_TEMP_PATH=(bool, False),
    DJANGO_CSRF_COOKIE_SECURE=(bool, True),
    DJANGO_DEBUG=(bool, False),
    DJANGO_EDC_BOOTSTRAP=(int, 3),
    DJANGO_EMAIL_ENABLED=(bool, False),
    DJANGO_EMAIL_USE_TLS=(bool, True),
    DJANGO_LIVE_SYSTEM=(bool, False),
    DJANGO_LOGGING_ENABLED=(bool, True),
    DJANGO_SESSION_COOKIE_SECURE=(bool, True),
    DJANGO_USE_I18N=(bool, False),
    DJANGO_USE_TZ=(bool, True),
    DEFENDER_ENABLED=(bool, False),
    EDC_LABEL_BROWSER_PRINT_PAGE_AUTO_BACK=(bool, True),
    TWILIO_ENABLED=(bool, False),
)

DEBUG = env("DJANGO_DEBUG")

if LOGGING_ENABLED := env("DJANGO_LOGGING_ENABLED"):
    from .logging import *  # noqa

BASE_DIR = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent)
ENV_DIR = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent)

# copy your .env file from .envs/ to BASE_DIR
if "test" in sys.argv:
    env.read_env(os.path.join(ENV_DIR, ".env-tests"))
    print(f"Reading env from {os.path.join(BASE_DIR, '.env-tests')}")
else:
    if not os.path.exists(os.path.join(ENV_DIR, ".env")):
        raise FileExistsError(
            f"Environment file does not exist. Got `{os.path.join(ENV_DIR, '.env')}`"
        )
    env.read_env(os.path.join(ENV_DIR, ".env"))

DEBUG = env("DJANGO_DEBUG")

SECRET_KEY = env.str("DJANGO_SECRET_KEY")

APP_NAME = env.str("DJANGO_APP_NAME")

LIVE_SYSTEM = env.str("DJANGO_LIVE_SYSTEM")

ETC_DIR = env.str("DJANGO_ETC_FOLDER")

TEST_DIR = os.path.join(BASE_DIR, APP_NAME, "tests")

# INTERNAL_IPS = ["127.0.0.1"] # for djdt
ALLOWED_HOSTS = ["*"]  # env.list('DJANGO_ALLOWED_HOSTS')

ENFORCE_RELATED_ACTION_ITEM_EXISTS = False

DEFAULT_APPOINTMENT_TYPE = "hospital"

LOGIN_URL = "/accounts/login/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

DEFENDER_ENABLED = env("DEFENDER_ENABLED")

INSTALLED_APPS = [
    "intecomm_edc.apps.AdminConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "defender",
    "multisite",
    "fontawesomefree",
    "django_crypto_fields.apps.AppConfig",
    "django_revision.apps.AppConfig",
    # "django_extensions",
    # "debug_toolbar",
    "logentry_admin",
    "simple_history",
    "storages",
    "edc_action_item.apps.AppConfig",
    "edc_appointment.apps.AppConfig",
    "edc_auth.apps.AppConfig",
    "edc_adverse_event.apps.AppConfig",
    "edc_consent.apps.AppConfig",
    "edc_crf.apps.AppConfig",
    "edc_reportable.apps.AppConfig",
    "edc_lab.apps.AppConfig",
    "edc_visit_schedule.apps.AppConfig",
    "edc_visit_tracking.apps.AppConfig",
    "edc_dx.apps.AppConfig",
    "edc_dx_review.apps.AppConfig",
    "edc_device.apps.AppConfig",
    "edc_dashboard.apps.AppConfig",
    "edc_data_manager.apps.AppConfig",
    "edc_export.apps.AppConfig",
    "edc_facility.apps.AppConfig",
    "edc_fieldsets.apps.AppConfig",
    "edc_form_validators.apps.AppConfig",
    "edc_he.apps.AppConfig",
    "edc_lab_dashboard.apps.AppConfig",
    "edc_label.apps.AppConfig",
    "edc_list_data.apps.AppConfig",
    "edc_listboard.apps.AppConfig",
    "edc_identifier.apps.AppConfig",
    "edc_locator.apps.AppConfig",
    "edc_metadata.apps.AppConfig",
    "edc_model.apps.AppConfig",
    "edc_model_fields.apps.AppConfig",
    "edc_model_admin.apps.AppConfig",
    "edc_navbar.apps.AppConfig",
    "edc_next_appointment.apps.AppConfig",
    "edc_notification.apps.AppConfig",
    "edc_offstudy.apps.AppConfig",
    "edc_pharmacy.apps.AppConfig",
    "edc_pdutils.apps.AppConfig",
    "edc_protocol.apps.AppConfig",
    "edc_protocol_incident.apps.AppConfig",
    "edc_prn.apps.AppConfig",
    "edc_qol.apps.AppConfig",
    "edc_randomization.apps.AppConfig",
    "edc_refusal.apps.AppConfig",
    "edc_registration.apps.AppConfig",
    "edc_pdf_reports.apps.AppConfig",
    "edc_review_dashboard.apps.AppConfig",
    "edc_rx.apps.AppConfig",
    "edc_screening.apps.AppConfig",
    "edc_sites.apps.AppConfig",
    "edc_subject_dashboard.apps.AppConfig",
    "edc_timepoint.apps.AppConfig",
    "edc_unblinding.apps.AppConfig",
    "edc_form_describer.apps.AppConfig",
    "edc_adherence.apps.AppConfig",
    "canned_views.apps.AppConfig",
    "intecomm_rando.apps.AppConfig",
    "intecomm_consent.apps.AppConfig",
    "intecomm_lists.apps.AppConfig",
    "intecomm_dashboard.apps.AppConfig",
    "intecomm_facility.apps.AppConfig",
    "intecomm_labs.apps.AppConfig",
    "intecomm_subject.apps.AppConfig",
    "intecomm_visit_schedule.apps.AppConfig",
    "intecomm_ae.apps.AppConfig",
    "intecomm_auth.apps.AppConfig",
    "intecomm_prn.apps.AppConfig",
    "intecomm_export.apps.AppConfig",
    "intecomm_group.apps.AppConfig",
    "intecomm_screening.apps.AppConfig",
    "intecomm_sites.apps.AppConfig",
    "intecomm_edc.apps.AppConfig",
]

if not DEFENDER_ENABLED:
    INSTALLED_APPS.pop(INSTALLED_APPS.index("defender"))

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "multisite.middleware.DynamicSiteMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "defender.middleware.FailedLoginMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if not DEFENDER_ENABLED:
    MIDDLEWARE.pop(MIDDLEWARE.index("defender.middleware.FailedLoginMiddleware"))

MIDDLEWARE.extend(
    [
        "edc_protocol.middleware.ProtocolMiddleware",
        "edc_dashboard.middleware.DashboardMiddleware",
        "edc_subject_dashboard.middleware.DashboardMiddleware",
        "edc_lab_dashboard.middleware.DashboardMiddleware",
        "edc_adverse_event.middleware.DashboardMiddleware",
        "edc_listboard.middleware.DashboardMiddleware",
        "edc_review_dashboard.middleware.DashboardMiddleware",
    ]
)

ROOT_URLCONF = f"{APP_NAME}.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "edc_model_admin.context_processors.admin_theme",
                "edc_constants.context_processor.constants",
                "edc_appointment.context_processors.constants",
                "edc_visit_tracking.context_processors.constants",
            ]
        },
    }
]

if env("DATABASE_SQLITE_ENABLED"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

else:
    DATABASES = {"default": env.db()}
# be secure and clear DATABASE_URL since it is no longer needed.
DATABASE_URL = None

if env.str("DJANGO_CACHE") == "redis":
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "PASSWORD": env.str("DJANGO_REDIS_PASSWORD"),
            },
            "KEY_PREFIX": f"{APP_NAME}",
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
    DJANGO_REDIS_IGNORE_EXCEPTIONS = True
    DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
elif env.str("DJANGO_CACHE") == "memcached":
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
            "LOCATION": "unix:/tmp/memcached.sock",
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

WSGI_APPLICATION = f"{APP_NAME}.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = ["edc_auth.backends.ModelBackendWithSite"]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 20},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Add custom languages not provided by Django
LANG_INFO = dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO)
django.conf.locale.LANG_INFO = LANG_INFO

LANGUAGE_CODE = "en"
LANGUAGE_LIST = ["sw", "en-gb", "en", "mas", "ry", "lg", "rny"]
LANGUAGES = [(code, LANG_INFO[code]["name"]) for code in LANGUAGE_LIST]
TIME_ZONE = env.str("DJANGO_TIME_ZONE")
DATE_INPUT_FORMATS = ["%Y-%m-%d", "%d/%m/%Y"]
DATETIME_INPUT_FORMATS = [
    "%Y-%m-%d %H:%M:%S",  # '2006-10-25 14:30:59'
    "%Y-%m-%d %H:%M:%S.%f",  # '2006-10-25 14:30:59.000200'
    "%Y-%m-%d %H:%M",  # '2006-10-25 14:30'
    "%Y-%m-%d",  # '2006-10-25'
    "%d/%m/%Y %H:%M:%S",  # '25/10/2006 14:30:59'
    "%d/%m/%Y %H:%M:%S.%f",  # '25/10/2006 14:30:59.000200'
    "%d/%m/%Y %H:%M",  # '25/10/2006 14:30'
    "%d/%m/%Y",  # '25/10/2006'
]
DATE_FORMAT = "j N Y"
DATETIME_FORMAT = "j N Y H:i"
SHORT_DATE_FORMAT = "d/m/Y"
SHORT_DATETIME_FORMAT = "d/m/Y H:i"

REPORT_DATETIME_FIELD_NAME = "report_datetime"

# See also any inte_* or edc_* apps.py
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# edc-appointment
EDC_APPOINTMENT_MAX_MONTHS_TO_NEXT_APPT = 7
EDC_APPOINTMENT_ALLOW_SKIPPED_APPT_USING = {
    "intecomm_subject.nextappointment": ("appt_date", "visitschedule")
}
EDC_APPOINTMENT_FORM_META_OPTIONS = {
    "labels": {"appt_type": "Where is the participant attending"},
    "help_texts": {
        "appt_type": (
            "If other than that expected based on subject's randomization, you will be "
            "asked to complete the `Changed location` CRF."
        )
    },
}

# edc-export
EDC_EXPORT_EXPORT_PII_USERS = env.list("EDC_EXPORT_EXPORT_PII_USERS")
EDC_FACILITY_HEALTH_FACILITY_MODEL = "intecomm_facility.healthfacility"

# edc-he
EDC_HE_ASSETS_MODEL = "intecomm_subject.healtheconomicsassets"
EDC_HE_HOUSEHOLDHEAD_MODEL = "intecomm_subject.healtheconomicshouseholdhead"
EDC_HE_INCOME_MODEL = "intecomm_subject.healtheconomicsincome"
EDC_HE_PATIENT_MODEL = "intecomm_subject.healtheconomicspatient"
EDC_HE_PROPERTY_MODEL = "intecomm_subject.healtheconomicsproperty"

# edc-pdutils
EXPORT_FILENAME_TIMESTAMP_FORMAT = "%Y%m%d"

# django_revision
REVISION = version(APP_NAME)

# enforce https if DEBUG=False!
# Note: will cause "CSRF verification failed. Request aborted"
#       if DEBUG=False and https not configured.
if not DEBUG:
    # CSFR cookies
    CSRF_COOKIE_SECURE = env.str("DJANGO_CSRF_COOKIE_SECURE")
    SECURE_PROXY_SSL_HEADER = env.tuple("DJANGO_SECURE_PROXY_SSL_HEADER")
    SESSION_COOKIE_SECURE = env.str("DJANGO_SESSION_COOKIE_SECURE")
    # other security defaults
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31_536_000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True

# edc_lab and label
LABEL_TEMPLATE_FOLDER = env.str("DJANGO_LABEL_TEMPLATE_FOLDER") or os.path.join(
    BASE_DIR, "label_templates", "2.25x1.25in"
)
CUPS_SERVERS = env.dict("DJANGO_CUPS_SERVERS")

LIST_MODEL_APP_LABEL = env.str("EDC_LIST_MODEL_APP_LABEL")
SUBJECT_APP_LABEL = env.str("EDC_SUBJECT_APP_LABEL")
SUBJECT_SCREENING_MODEL = env.str("EDC_SUBJECT_SCREENING_MODEL")
SUBJECT_CONSENT_MODEL = env.str("EDC_SUBJECT_CONSENT_MODEL")
SUBJECT_LOCATOR_MODEL = "intecomm_prn.subjectlocator"
SUBJECT_REFUSAL_MODEL = env.str("EDC_REFUSAL_SUBJECT_REFUSAL_MODEL")
SUBJECT_REQUISITION_MODEL = env.str("EDC_SUBJECT_REQUISITION_MODEL")
SUBJECT_VISIT_MODEL = env.str("EDC_SUBJECT_VISIT_MODEL")
SUBJECT_VISIT_MISSED_MODEL = env.str("EDC_SUBJECT_VISIT_MISSED_MODEL")
SUBJECT_VISIT_MISSED_REASONS_MODEL = env.str("EDC_SUBJECT_VISIT_MISSED_REASONS_MODEL")
EDC_BLOOD_RESULTS_MODEL_APP_LABEL = "intecomm_subject"

EDC_NAVBAR_DEFAULT = env("EDC_NAVBAR_DEFAULT")

# dashboards
EDC_BOOTSTRAP = env("DJANGO_EDC_BOOTSTRAP")
DASHBOARD_URL_NAMES = env.dict("DJANGO_DASHBOARD_URL_NAMES")
DASHBOARD_BASE_TEMPLATES = env.dict("DJANGO_DASHBOARD_BASE_TEMPLATES")
LAB_DASHBOARD_BASE_TEMPLATES = env.dict("DJANGO_LAB_DASHBOARD_BASE_TEMPLATES")
LAB_DASHBOARD_URL_NAMES = env.dict("DJANGO_LAB_DASHBOARD_URL_NAMES")

# edc-consent
EDC_CONSENT_REMOVE_PATIENT_NAMES_FROM_COUNTRIES = env.list(
    "EDC_CONSENT_REMOVE_PATIENT_NAMES_FROM_COUNTRIES", default=[]
)

# edc-diagnosis
EDC_DX_LABELS = dict(hiv="HIV", dm="Diabetes", htn="Hypertension")

# edc-dx-review
EDC_DX_REVIEW_APP_LABEL = "intecomm_subject"
EDC_DX_REVIEW_LIST_MODEL_APP_LABEL = "edc_dx_review"
# edc_facility
HOLIDAY_FILE = env.str("DJANGO_HOLIDAY_FILE")

# edc-label
EDC_LABEL_BROWSER_PRINT_PAGE_AUTO_BACK = env("EDC_LABEL_BROWSER_PRINT_PAGE_AUTO_BACK")

# edc_model_admin
EDC_MODEL_ADMIN_CSS_THEME = "edc_indigo"

EDC_OFFSTUDY_OFFSTUDY_MODEL = "intecomm_prn.endofstudy"

# edc-protocol-incident
EDC_PROTOCOL_VIOLATION_TYPE = PROTOCOL_INCIDENT

# edc_randomization

EDC_RANDOMIZATION_UNBLINDED_USERS = env.list("EDC_RANDOMIZATION_UNBLINDED_USERS")
EDC_RANDOMIZATION_REGISTER_DEFAULT_RANDOMIZER = False
EDC_RANDOMIZATION_SKIP_VERIFY_CHECKS = True
EDC_RANDOMIZATION_LIST_PATH = env.str("EDC_RANDOMIZATION_LIST_PATH")

# edc-sites
EDC_SITES_MODULE_NAME = env.str("EDC_SITES_MODULE_NAME")

# django-multisite
CACHE_MULTISITE_KEY_PREFIX = APP_NAME
SILENCED_SYSTEM_CHECKS = ["sites.E101"]

# django-defender
# see if env.str("DJANGO_CACHE") == "redis" above
# and that redis server is running
DEFENDER_REDIS_NAME = "default"
DEFENDER_LOCK_OUT_BY_IP_AND_USERNAME = True
DEFENDER_LOCKOUT_TEMPLATE = "edc_auth/bootstrap3/login.html"
DEFENDER_LOGIN_FAILURE_LIMIT = 5

# edc_crf
CRF_STATUS_DEFAULT = COMPLETE

EMAIL_ENABLED = env("DJANGO_EMAIL_ENABLED")
EMAIL_CONTACTS = env.dict("DJANGO_EMAIL_CONTACTS")
if EMAIL_ENABLED:
    EMAIL_HOST = env.str("DJANGO_EMAIL_HOST")
    EMAIL_PORT = env.int("DJANGO_EMAIL_PORT")
    EMAIL_HOST_USER = env.str("DJANGO_EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env.str("DJANGO_EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = env("DJANGO_EMAIL_USE_TLS")
    MAILGUN_API_KEY = env("MAILGUN_API_KEY")
    MAILGUN_API_URL = env("MAILGUN_API_URL")

# django_revision
GIT_DIR = BASE_DIR

# django_crypto_fields
KEY_PATH = env.str("DJANGO_KEY_FOLDER")
AUTO_CREATE_KEYS = env("DJANGO_AUTO_CREATE_KEYS")

EXPORT_FOLDER = env.str("DJANGO_EXPORT_FOLDER") or os.path.expanduser("~/")

# django_simple_history
SIMPLE_HISTORY_ENFORCE_HISTORY_MODEL_PERMISSIONS = True

FQDN = env.str("DJANGO_FQDN")  # ???
INDEX_PAGE = env.str("DJANGO_INDEX_PAGE")
INDEX_PAGE_LABEL = env.str("DJANGO_INDEX_PAGE_LABEL")

# edc_adverse_event
ADVERSE_EVENT_ADMIN_SITE = env.str("EDC_ADVERSE_EVENT_ADMIN_SITE")
ADVERSE_EVENT_APP_LABEL = env.str("EDC_ADVERSE_EVENT_APP_LABEL")

# edc_data_manager
DATA_DICTIONARY_APP_LABELS = [
    "intecomm_consent",
    "intecomm_subject",
    "intecomm_prn",
    "intecomm_screening",
    "intecomm_ae",
    "edc_appointment",
    "edc_locator",
    "edc_offstudy",
]

# edc_protocol
EDC_PROTOCOL = env.str("EDC_PROTOCOL")
EDC_PROTOCOL_INSTITUTION_NAME = env.str("EDC_PROTOCOL_INSTITUTION_NAME")
EDC_PROTOCOL_NUMBER = env.str("EDC_PROTOCOL_NUMBER")
# EDC_PROTOCOL_PROJECT_NAME = env.str("EDC_PROTOCOL_PROJECT_NAME")
EDC_PROTOCOL_PROJECT_NAME = "INTECOMM"
EDC_PROTOCOL_STUDY_OPEN_DATETIME = get_datetime_from_env(
    *env.list("EDC_PROTOCOL_STUDY_OPEN_DATETIME")
)
EDC_PROTOCOL_STUDY_CLOSE_DATETIME = get_datetime_from_env(
    *env.list("EDC_PROTOCOL_STUDY_CLOSE_DATETIME")
)
EDC_PROTOCOL_TITLE = env.str("EDC_PROTOCOL_TITLE")

# static / AWS
if env("AWS_ENABLED"):
    # see
    # https://www.digitalocean.com/community/tutorials/
    # how-to-set-up-a-scalable-django-app-with-digitalocean-
    # managed-databases-and-spaces
    AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
    AWS_DEFAULT_ACL = "public-read"
    AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_CUSTOM_DOMAIN = env.str("AWS_S3_CUSTOM_DOMAIN")
    AWS_S3_ENDPOINT_URL = env.str("AWS_S3_ENDPOINT_URL")
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_LOCATION = env.str("AWS_LOCATION")
    AWS_IS_GZIPPED = True
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATIC_URL = f"{os.path.join(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)}/"
    STATIC_ROOT = ""
elif DEBUG:
    STATIC_URL = "static/"  # env.str("DJANGO_STATIC_URL")
    STATIC_ROOT = env.str("DJANGO_STATIC_ROOT") or os.path.expanduser(
        "~/source/edc_source/intecomm-edc/static/"
    )
else:
    # run collectstatic, check nginx LOCATION
    STATIC_URL = env.str("DJANGO_STATIC_URL")
    STATIC_ROOT = env.str("DJANGO_STATIC_ROOT")

# CELERY

if "test" in sys.argv:

    class DisableMigrations:
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()
    PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
    DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"


INTECOMM_MIN_GROUP_SIZE = 14
INTECOMM_MIN_GROUP_SIZE_FOR_RATIO = 9
