import datetime as dt
from zoneinfo import ZoneInfo

import time_machine
from dateutil.relativedelta import relativedelta
from django.test import TestCase, override_settings
from edc_constants.constants import HIV, NOT_APPLICABLE, YES
from edc_metadata import REQUIRED
from edc_pdutils.constants import SYSTEM_COLUMNS
from edc_utils import get_utcnow
from model_bakery import baker

from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin
from intecomm_subject.forms import HivReviewForm
from intecomm_subject.models import ClinicalReview

utc_tz = ZoneInfo("UTC")


@time_machine.travel(dt.datetime(2019, 5, 11, 8, 00, tzinfo=utc_tz))
class TestInitialAndReview(IntecommTestCaseMixin, TestCase):
    """These tests cover funcs/methods that access other models such
    as SubjectConsent, SubjectScreening ... .

    More tests are in the `intecomm_form_validators` module.
    """

    patient_group = None

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.patient_group = cls.get_randomized_patient_group(
            report_datetime=get_utcnow() - relativedelta(days=10)
        )

    def setUp(self):
        self.assertTrue(self.patient_group.randomized)

    @override_settings(EDC_MODEL_REPORT_DATETIME_FIELD_NAME="report_datetime")
    def test_ok(self):
        patient_log = self.patient_group.patients.filter(conditions__name__in=[HIV]).first()
        subject_visit = self.get_subject_visit(
            subject_identifier=patient_log.subject_identifier
        )

        self.get_or_create_clinical_review_baseline(patient_log, subject_visit)
        self.assertTrue(
            self.get_crf_metadata(
                subject_visit, model="intecomm_subject.hivinitialreview", entry_status=REQUIRED
            )
        )
        # report rx_init and rx_init_date
        baker.make_recipe(
            "intecomm_subject.hivinitialreview",
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            rx_init=YES,
            rx_init_date=subject_visit.report_datetime - relativedelta(years=5),
        )

        # go to next visit
        subject_visit = self.get_next_subject_visit(subject_visit)
        traveller = time_machine.travel(subject_visit.report_datetime)
        traveller.start()

        obj = baker.prepare_recipe(
            "intecomm_subject.hivreview",
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
        )
        excluded_columns = ["id", "consent_model", "consent_version"]
        excluded_columns.extend(SYSTEM_COLUMNS)
        cleaned_data = {
            k: v
            for k, v in obj.__dict__.items()
            if k not in excluded_columns
            and not k.startswith("_")
            and k not in ["rx_init_estimated_data"]
        }

        # try to submit without clinical review
        cleaned_data.update(
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            rx_init=YES,
            rx_init_date=subject_visit.report_datetime - relativedelta(years=5),
        )
        form = HivReviewForm(data=cleaned_data)

        form.is_valid()

        self.assertIn(ClinicalReview._meta.verbose_name, str(form._errors.get("__all__")))

        # submit clinical review
        clinicalreview_obj = baker.make_recipe(
            "intecomm_subject.clinicalreview",
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            hiv_test=NOT_APPLICABLE,
        )

        # incorrectly try to report rx_init date already reported on initial_review
        cleaned_data.update(
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            rx_init=YES,
            rx_init_date=subject_visit.report_datetime - relativedelta(years=5),
            site=clinicalreview_obj.site,
        )
        form = HivReviewForm(data=cleaned_data)

        form.is_valid()

        self.assertIn("rx_init", form._errors)

        # ok
        cleaned_data.update(
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            rx_init=NOT_APPLICABLE,
            rx_init_date=None,
            site=clinicalreview_obj.site,
        )
        form = HivReviewForm(data=cleaned_data)

        form.is_valid()

        self.assertEqual(form._errors or {}, {})
