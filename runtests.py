#!/usr/bin/env python
import logging
from datetime import datetime
from os.path import abspath, dirname, join
from zoneinfo import ZoneInfo

import django
from edc_constants.internationalization import EXTRA_LANG_INFO
from edc_test_utils import DefaultTestSettings, func_main
from multisite import SiteID

app_name = "intecomm_edc"
base_dir = dirname(abspath(__file__))
LANG_INFO = dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO)
django.conf.locale.LANG_INFO = LANG_INFO
LANGUAGE_LIST = ["sw", "en-gb", "en", "mas", "ry", "lg", "rny"]


project_settings = DefaultTestSettings(
    calling_file=__file__,
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
    LANGUAGES=[(code, LANG_INFO[code]["name"]) for code in LANGUAGE_LIST],
    EXPORT_FOLDER=join(base_dir, "tests", "export"),
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
        2023, 12, 31, 23, 59, 59, tzinfo=ZoneInfo("UTC")
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
        community_subject_listboard_template=(
            "intecomm_dashboard/bootstrap3/subject/community_listboard.html"
        ),
        facility_subject_listboard_template=(
            "intecomm_dashboard/bootstrap3/subject/facility_listboard.html"
        ),
        subject_dashboard_template="intecomm_dashboard/subject/dashboard.html",
        subject_review_listboard_template="edc_review_dashboard/subject_review_listboard.html",
    ),
    ETC_DIR=join(base_dir, "intecomm_edc", "tests", "etc"),
    EDC_BOOTSTRAP=3,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    EMAIL_CONTACTS={
        "data_request": "someone@example.com",
        "data_manager": "someone@example.com",
        "tmg": "someone@example.com",
    },
    EMAIL_ENABLED=True,
    HOLIDAY_FILE=join(base_dir, "intecomm_edc", "tests", "holidays.csv"),
    LIVE_SYSTEM=False,
    EDC_RANDOMIZATION_LIST_PATH=join(base_dir, "intecomm_edc", "tests", "etc"),
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
        "django_revision.apps.AppConfig",
        # "debug_toolbar",
        "django_extensions",
        "logentry_admin",
        "multisite",
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
    ],
    add_dashboard_middleware=True,
    add_lab_dashboard_middleware=True,
    add_adverse_event_dashboard_middleware=True,
    # add_multisite_middleware=True,
).settings


def main():
    tests = [
        "intecomm_auth.tests",
        "intecomm_ae.tests",
        "intecomm_dashboard.tests",
        "intecomm_edc.tests",
        "intecomm_labs.tests",
        "intecomm_lists.tests",
        "intecomm_prn.tests",
        "intecomm_group.tests",
        "intecomm_screening.tests",
        "intecomm_subject.tests",
        "intecomm_consent.tests",
        "intecomm_visit_schedule.tests",
        "intecomm_form_validators.tests",
        "intecomm_rando.tests",
        "intecomm_eligibility.tests",
    ]

    func_main(project_settings, *tests)


if __name__ == "__main__":
    logging.basicConfig()
    main()
