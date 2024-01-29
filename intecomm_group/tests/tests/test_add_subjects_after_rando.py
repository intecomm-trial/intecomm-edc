import datetime as dt
import io
import os
import sys
from zoneinfo import ZoneInfo

import time_machine
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.test import TestCase, override_settings
from edc_constants.constants import DM, HIV, HTN
from edc_randomization.site_randomizers import site_randomizers
from edc_utils import get_utcnow
from intecomm_form_validators import IN_FOLLOWUP
from intecomm_rando.models import RandomizationList
from intecomm_rando.randomizers import Randomizer
from intecomm_rando.utils import get_assignment_for_subject

from intecomm_group.models import PatientGroup
from intecomm_group.utils import add_subjects_to_group
from intecomm_screening.models import PatientLog
from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin

utc_tz = ZoneInfo("UTC")


@override_settings(
    EDC_RANDOMIZATION_LIST_PATH=os.path.join(
        settings.BASE_DIR, "intecomm_subject", "tests", "etc", "community_only"
    )
)
@time_machine.travel(dt.datetime(2019, 5, 11, 8, 00, tzinfo=utc_tz))
class TestAddToCommunityArmGroup(IntecommTestCaseMixin, TestCase):
    patient_group = None
    import_randomization_list = False
    sid_count_for_tests = 2
    report_datetime: dt.datetime = None
    patient_group_name = "BRANDX"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.report_datetime = get_utcnow() - relativedelta(days=10)
        site_randomizers._registry = {}
        Randomizer.randomizationlist_folder = settings.EDC_RANDOMIZATION_LIST_PATH
        site_randomizers.register(Randomizer)
        randomizer_cls = site_randomizers.get("default")
        randomizer_cls.import_list(verbose=False, sid_count_for_tests=cls.sid_count_for_tests)
        cls.patient_group = cls.get_randomized_patient_group(
            report_datetime=cls.report_datetime, group_name=cls.patient_group_name
        )

    def setUp(self):
        self.assertTrue(self.patient_group.randomized)
        patient_log = self.patient_group.patients.filter(conditions__name__in=[HTN]).first()
        self.subject_identifier = patient_log.subject_identifier

    def test_add_subjects_to_group(self):
        patient_group = PatientGroup.objects.get(name=self.patient_group_name)
        assignment = RandomizationList.objects.get(
            group_identifier=patient_group.group_identifier
        ).assignment

        self.assertEqual(patient_group.status, IN_FOLLOWUP)
        patient_count = patient_group.patients.all().count()
        hiv_count = (
            patient_group.patients.filter(conditions__name__in=[HIV])
            .exclude(conditions__name__in=[HTN, DM])
            .count()
        )
        htn_count = (
            patient_group.patients.filter(conditions__name__in=[HTN])
            .exclude(conditions__name__in=[HIV, DM])
            .count()
        )
        dm_count = (
            patient_group.patients.filter(conditions__name__in=[DM])
            .exclude(conditions__name__in=[HIV, HTN])
            .count()
        )

        pat1 = self.get_consented_patient(
            condition_name=HIV, report_datetime=self.report_datetime
        )
        pat2 = self.get_consented_patient(
            condition_name=HTN, report_datetime=self.report_datetime
        )
        pat3 = self.get_consented_patient(
            condition_name=DM, report_datetime=self.report_datetime
        )
        subject_identifiers = [
            pat1.subject_identifier,
            pat2.subject_identifier,
            pat3.subject_identifier,
        ]
        add_subjects_to_group(self.patient_group_name, subject_identifiers)

        patient_group = PatientGroup.objects.get(name=self.patient_group_name)
        self.assertEqual(patient_group.patients.all().count(), patient_count + 3)

        new_hiv_count = (
            patient_group.patients.filter(conditions__name__in=[HIV])
            .exclude(conditions__name__in=[HTN, DM])
            .count()
        )
        new_htn_count = (
            patient_group.patients.filter(conditions__name__in=[HTN])
            .exclude(conditions__name__in=[HIV, DM])
            .count()
        )
        new_dm_count = (
            patient_group.patients.filter(conditions__name__in=[DM])
            .exclude(conditions__name__in=[HIV, HTN])
            .count()
        )

        self.assertEqual(patient_group.patients.all().count(), patient_count + 3)
        self.assertEqual(dm_count + 1, new_dm_count)
        self.assertEqual(htn_count + 1, new_htn_count)
        self.assertEqual(hiv_count + 1, new_hiv_count)
        self.assertEqual(patient_group.status, IN_FOLLOWUP)

        for subject_identifier in subject_identifiers:
            obj = PatientLog.objects.get(subject_identifier=subject_identifier)
            self.assertEqual(obj.group_identifier, patient_group.group_identifier)
            self.assertEqual(get_assignment_for_subject(subject_identifier), assignment)

        # try to add again
        add_subjects_to_group(self.patient_group_name, subject_identifiers)

        # no change
        self.assertEqual(patient_group.patients.all().count(), patient_count + 3)
        self.assertEqual(dm_count + 1, new_dm_count)
        self.assertEqual(htn_count + 1, new_htn_count)
        self.assertEqual(hiv_count + 1, new_hiv_count)
        self.assertEqual(patient_group.status, IN_FOLLOWUP)

        # try unknown group
        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            add_subjects_to_group("BLAH", subject_identifiers)
        finally:
            sys.stdout = sys.__stdout__
            self.assertIn("PatientGroup does not exist", captured_output.getvalue())

        # try unknown subject
        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            add_subjects_to_group(self.patient_group_name, ["1234"])
        finally:
            sys.stdout = sys.__stdout__
            self.assertIn("skipping", captured_output.getvalue())
