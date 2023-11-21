import datetime as dt
import os
from zoneinfo import ZoneInfo

import time_machine
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, override_settings
from edc_appointment.models import Appointment, AppointmentType
from edc_constants.constants import CLINIC, COMMUNITY, HTN
from edc_metadata import REQUIRED
from edc_metadata.models import CrfMetadata
from edc_randomization.site_randomizers import site_randomizers
from edc_utils import get_utcnow
from edc_visit_tracking.constants import SCHEDULED
from intecomm_rando.constants import COMMUNITY_ARM
from intecomm_rando.randomizers import Randomizer
from intecomm_rando.utils import get_assignment_for_subject

from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin
from intecomm_subject.models import SubjectVisit

utc_tz = ZoneInfo("UTC")


@override_settings(
    EDC_RANDOMIZATION_LIST_PATH=os.path.join(
        settings.BASE_DIR, "intecomm_subject", "tests", "etc", "community_only"
    )
)
@time_machine.travel(dt.datetime(2019, 5, 11, 8, 00, tzinfo=utc_tz))
class TestLocationUpdate(IntecommTestCaseMixin, TestCase):
    patient_group = None
    import_randomization_list = False
    sid_count_for_tests = 2

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        site_randomizers._registry = {}
        Randomizer.randomizationlist_folder = settings.EDC_RANDOMIZATION_LIST_PATH
        site_randomizers.register(Randomizer)
        randomizer_cls = site_randomizers.get("default")
        randomizer_cls.import_list(verbose=False, sid_count_for_tests=cls.sid_count_for_tests)
        cls.patient_group = cls.get_randomized_patient_group(
            report_datetime=get_utcnow() - relativedelta(days=10), group_name="BRANDX"
        )

    def setUp(self):
        self.assertTrue(self.patient_group.randomized)

    def test_crf_metadata(self):
        patient_log = self.patient_group.patients.filter(conditions__name__in=[HTN]).first()
        self.get_subject_visit(subject_identifier=patient_log.subject_identifier)
        subject_visit = self.get_subject_visit(
            subject_identifier=patient_log.subject_identifier, visit_code="1010"
        )

        self.assertEqual(
            get_assignment_for_subject(subject_visit.subject_identifier), COMMUNITY_ARM
        )
        appointment = Appointment.objects.get(
            subject_identifier=subject_visit.subject_identifier, visit_code="1020"
        )
        appointment.appt_type = AppointmentType.objects.get(name=COMMUNITY)
        appointment.save()
        subject_visit = SubjectVisit.objects.create(
            appointment=appointment,
            report_datetime=appointment.appt_datetime,
            reason=SCHEDULED,
        )
        try:
            CrfMetadata.objects.get(
                subject_identifier=subject_visit.subject_identifier,
                visit_code=subject_visit.visit_code,
                model="intecomm_subject.locationupdate",
                entry_status=REQUIRED,
            )
        except ObjectDoesNotExist:
            pass
        else:
            self.fail("CrfMetadata for `intecomm_subject.locationupdate` unexpectedly exists")

        appointment.appt_type = AppointmentType.objects.get(name=CLINIC)  # facility
        appointment.save()
        subject_visit.save()
        try:
            CrfMetadata.objects.get(
                subject_identifier=subject_visit.subject_identifier,
                visit_code=subject_visit.visit_code,
                model="intecomm_subject.locationupdate",
                entry_status=REQUIRED,
            )
        except ObjectDoesNotExist:
            self.fail(
                "CrfMetadata for `intecomm_subject.locationupdate` unexpectedly does not exist"
            )
