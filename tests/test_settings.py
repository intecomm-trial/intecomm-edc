#!/usr/bin/env python
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from django.conf import locale
from edc_constants.internationalization import EXTRA_LANG_INFO
from edc_test_settings.default_test_settings import DefaultTestSettings
from multisite import SiteID

lang_info = dict(locale.LANG_INFO, **EXTRA_LANG_INFO)
locale.LANG_INFO = dict(locale.LANG_INFO, **EXTRA_LANG_INFO)

app_name = "intecomm_edc"
base_dir = Path(__file__).absolute().parent.parent


def get_languages():
    return [
        (code, lang_info[code]["name"])
        for code in ["sw", "en-gb", "en", "mas", "ry", "lg", "rny"]
    ]


project_settings = DefaultTestSettings(
    calling_file=__file__,
    SILENCED_SYSTEM_CHECKS=["sites.E101", "edc_navbar.E002", "edc_navbar.E003"],
    EDC_EGFR_DROP_NOTIFICATION_MODEL="intecomm_subject.egfrdropnotification",
    EDC_RANDOMIZATION_REGISTER_DEFAULT_RANDOMIZER=False,
    ROOT_URLCONF="intecomm_edc.urls",
    EDC_AUTH_CODENAMES_WARN_ONLY=True,
    EDC_DX_REVIEW_LIST_MODEL_APP_LABEL="edc_dx_review",
    EDC_DX_REVIEW_APP_LABEL="intecomm_subject",
    EDC_APPOINTMENT_ALLOW_SKIPPED_APPT_USING={
        "intecomm_subject.nextappointment": ("appt_date", "visitschedule")
    },
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    SITE_ID=SiteID(default=101),
    SENTRY_ENABLED=False,
    INDEX_PAGE="localhost:8000",
    LANGUAGE_CODE="en",
    LANGUAGES=get_languages(),
    EXPORT_FOLDER=str(base_dir / "tests" / "export"),
    SUBJECT_APP_LABEL="intecomm_subject",
    SUBJECT_SCREENING_MODEL="intecomm_screening.subjectscreening",
    SUBJECT_VISIT_MODEL="intecomm_subject.subjectvisit",
    SUBJECT_VISIT_MISSED_MODEL="intecomm_subject.subjectvisitmissed",
    SUBJECT_CONSENT_MODEL="intecomm_consent.subjectconsent",
    SUBJECT_REQUISITION_MODEL="intecomm_subject.subjectrequisition",
    SUBJECT_LOCATOR_MODEL="intecomm_prn.subjectlocator",
    EDC_HE_ASSETS_MODEL="intecomm_subject.healtheconomicsassets",
    EDC_HE_HOUSEHOLDHEAD_MODEL="intecomm_subject.healtheconomicshouseholdhead",
    EDC_HE_INCOME_MODEL="intecomm_subject.healtheconomicsincome",
    EDC_HE_PATIENT_MODEL="intecomm_subject.healtheconomicspatient",
    EDC_HE_PROPERTY_MODEL="intecomm_subject.healtheconomicsproperty",
    EDC_BLOOD_RESULTS_MODEL_APP_LABEL="intecomm_subject",
    DEFENDER_ENABLED=False,
    DJANGO_LAB_DASHBOARD_REQUISITION_MODEL="intecomm_subject.subjectrequisition",
    ADVERSE_EVENT_ADMIN_SITE="intecomm_ae_admin",
    EDC_DX_LABELS=dict(hiv="HIV", dm="Diabetes", htn="Hypertension"),
    ADVERSE_EVENT_APP_LABEL="intecomm_ae",
    EDC_NAVBAR_DEFAULT="intecomm_dashboard",
    EDC_PROTOCOL_STUDY_OPEN_DATETIME=datetime(2019, 4, 30, 0, 0, 0, tzinfo=ZoneInfo("UTC")),
    EDC_PROTOCOL_STUDY_CLOSE_DATETIME=datetime(
        2025, 12, 31, 23, 59, 59, tzinfo=ZoneInfo("UTC")
    ),
    DJANGO_LANGUAGES=dict(
        en="English",
        lg="Luganda",
        rny="Runyankore",
        ry="Runyakitara",
        mas="Maasai",
    ),
    DASHBOARD_BASE_TEMPLATES=dict(
        edc_base_template="edc_dashboard/base.html",
        listboard_base_template="intecomm_edc/base.html",
        dashboard_base_template="intecomm_edc/base.html",
        screening_listboard_template="intecomm_dashboard/screening/listboard.html",
        subject_listboard_template=(
            "intecomm_dashboard/bootstrap3/subject/subject_listboard.html"
        ),
        subject_dashboard_template="intecomm_dashboard/subject/dashboard.html",
        subject_review_listboard_template="edc_review_dashboard/subject_review_listboard.html",
    ),
    ETC_DIR=base_dir / "tests" / "etc",
    EDC_BOOTSTRAP=3,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    EMAIL_CONTACTS={
        "data_request": "someone@example.com",
        "data_manager": "someone@example.com",
        "tmg": "someone@example.com",
        "ae_reports": "aereports@example.com",
    },
    EMAIL_ENABLED=True,
    HOLIDAY_FILE=str(base_dir / "intecomm_edc" / "tests" / "holidays.csv"),
    LIVE_SYSTEM=False,
    EDC_RANDOMIZATION_LIST_PATH=str(base_dir / "intecomm_edc" / "tests" / "etc"),
    EDC_SITES_MODULE_NAME="intecomm_sites",
    EDC_AUTH_SKIP_SITE_AUTHS=True,
    EDC_AUTH_SKIP_AUTH_UPDATER=True,
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "django_crypto_fields.apps.AppConfig",
        "django_pylabels.apps.AppConfig",
        "django_revision.apps.AppConfig",
        # "debug_toolbar",
        "django_extensions",
        "logentry_admin",
        "multisite",
        "simple_history",
        "storages",
        "edc_sites.apps.AppConfig",
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
        "edc_form_runners.apps.AppConfig",
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
        "edc_next_appointment.apps.AppConfig",  # keep for migrate
        "edc_notification.apps.AppConfig",
        "edc_offstudy.apps.AppConfig",
        "edc_pharmacy.apps.AppConfig",
        "edc_pdutils.apps.AppConfig",
        "edc_protocol.apps.AppConfig",
        "edc_protocol_incident.apps.AppConfig",
        "edc_prn.apps.AppConfig",
        "edc_pylabels.apps.AppConfig",
        "edc_qol.apps.AppConfig",
        "edc_randomization.apps.AppConfig",
        "edc_refusal.apps.AppConfig",
        "edc_registration.apps.AppConfig",
        "edc_pdf_reports.apps.AppConfig",
        "edc_review_dashboard.apps.AppConfig",
        "edc_rx.apps.AppConfig",
        "edc_screening.apps.AppConfig",
        "edc_subject_dashboard.apps.AppConfig",
        "edc_timepoint.apps.AppConfig",
        "edc_unblinding.apps.AppConfig",
        "edc_form_describer.apps.AppConfig",
        "edc_adherence.apps.AppConfig",
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
        "edc_appconfig.apps.AppConfig",
    ],
    add_dashboard_middleware=True,
    add_lab_dashboard_middleware=True,
    add_adverse_event_dashboard_middleware=True,
).settings

for k, v in project_settings.items():
    setattr(sys.modules[__name__], k, v)
