import datetime as dt
import os
from zoneinfo import ZoneInfo

import time_machine
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.sites.models import Site
from django.test import TestCase, override_settings, tag
from edc_appointment.constants import INCOMPLETE_APPT, ONTIME_APPT, SKIPPED_APPT
from edc_appointment.models import Appointment, AppointmentType
from edc_constants.constants import COMMUNITY, COMPLETE, HTN, NOT_APPLICABLE
from edc_pharmacy.constants import IN_PROGRESS_APPT
from edc_randomization.site_randomizers import site_randomizers
from edc_timepoint.constants import OPEN_TIMEPOINT
from edc_utils import get_utcnow
from edc_visit_tracking.constants import SCHEDULED
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM
from intecomm_rando.randomizers import Randomizer
from intecomm_rando.utils import get_assignment_for_subject

from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin
from intecomm_subject.admin.appointment_admin import AppointmentForm
from intecomm_subject.models import SubjectVisit

utc_tz = ZoneInfo("UTC")


@override_settings(
    EDC_RANDOMIZATION_LIST_PATH=os.path.join(
        settings.BASE_DIR, "intecomm_subject", "tests", "etc", "community_only"
    )
)
@time_machine.travel(dt.datetime(2019, 5, 11, 8, 00, tzinfo=utc_tz))
class TestAppointmentCommunityArm(IntecommTestCaseMixin, TestCase):
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
        patient_log = self.patient_group.patients.filter(conditions__name__in=[HTN]).first()
        self.subject_identifier = patient_log.subject_identifier

    def update_appt_1000(self):
        appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code="1000"
        )
        SubjectVisit.objects.create(
            appointment=appointment,
            report_datetime=appointment.appt_datetime,
            reason=SCHEDULED,
        )
        appointment.appt_status = INCOMPLETE_APPT
        appointment.save()
        appointment.refresh_from_db()

    @staticmethod
    def get_default_appt_data(appointment):
        return dict(
            subject_identifier=appointment.subject_identifier,
            timepoint=appointment.timepoint,
            timepoint_datetime=appointment.timepoint_datetime,
            timepoint_status=OPEN_TIMEPOINT,
            visit_code=appointment.visit_code,
            visit_code_sequence=appointment.visit_code_sequence,
            facility_name=appointment.facility_name,
            document_status=COMPLETE,
            appt_close_datetime=appointment.appt_datetime,
            appt_datetime=appointment.appt_datetime,
            appt_reason=appointment.appt_reason,
            appt_timing=ONTIME_APPT,
            appt_type=AppointmentType.objects.get(name=COMMUNITY),
            appt_status=IN_PROGRESS_APPT,
            site=Site.objects.get(id=settings.SITE_ID),
        )

    @tag("1")
    @time_machine.travel(dt.datetime(2019, 5, 11, 8, 00, tzinfo=utc_tz))
    def test_ok(self):
        self.update_appt_1000()
        appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code="1010"
        )
        traveller = time_machine.travel(appointment.appt_datetime + relativedelta(days=3))
        traveller.start()
        self.assertEqual(
            get_assignment_for_subject(appointment.subject_identifier), COMMUNITY_ARM
        )
        data = self.get_default_appt_data(appointment)
        form = AppointmentForm(data=data, instance=appointment)
        form.is_valid()
        self.assertEqual({}, form._errors)

    @tag("1")
    @time_machine.travel(dt.datetime(2019, 5, 11, 8, 00, tzinfo=utc_tz))
    def test_appt_may_not_be_skipped_in_community_arm(self):
        self.update_appt_1000()
        appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code="1010"
        )
        traveller = time_machine.travel(appointment.appt_datetime + relativedelta(days=3))
        traveller.start()
        self.assertEqual(
            get_assignment_for_subject(appointment.subject_identifier), COMMUNITY_ARM
        )

        data = self.get_default_appt_data(appointment)
        data.update(
            appt_status=SKIPPED_APPT,
            appt_type=AppointmentType.objects.get(name=NOT_APPLICABLE),
            appt_timing=NOT_APPLICABLE,
        )
        form = AppointmentForm(data=data, instance=appointment)
        form.is_valid()
        self.assertIn("appt_status", form._errors)
        self.assertIn(
            "Community appointments may not be skipped", str(form._errors.get("appt_status"))
        )


@override_settings(
    EDC_RANDOMIZATION_LIST_PATH=os.path.join(
        settings.BASE_DIR, "intecomm_subject", "tests", "etc", "facility_only"
    ),
    EDC_RANDOMIZATION_REGISTER_DEFAULT_RANDOMIZER=False,
)
@time_machine.travel(dt.datetime(2019, 5, 11, 8, 00, tzinfo=utc_tz))
class TestAppointmentFacilityArm(IntecommTestCaseMixin, TestCase):
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
        patient_log = self.patient_group.patients.filter(conditions__name__in=[HTN]).first()
        self.subject_identifier = patient_log.subject_identifier

    def update_appt_1000(self):
        appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code="1000"
        )
        SubjectVisit.objects.create(
            appointment=appointment,
            report_datetime=appointment.appt_datetime,
            reason=SCHEDULED,
        )
        appointment.appt_status = INCOMPLETE_APPT
        appointment.save()
        appointment.refresh_from_db()

    @staticmethod
    def get_default_appt_data(appointment):
        return dict(
            subject_identifier=appointment.subject_identifier,
            timepoint=appointment.timepoint,
            timepoint_datetime=appointment.timepoint_datetime,
            timepoint_status=OPEN_TIMEPOINT,
            visit_code=appointment.visit_code,
            visit_code_sequence=appointment.visit_code_sequence,
            facility_name=appointment.facility_name,
            document_status=COMPLETE,
            appt_close_datetime=appointment.appt_datetime,
            appt_datetime=appointment.appt_datetime,
            appt_reason=appointment.appt_reason,
            appt_timing=ONTIME_APPT,
            appt_type=AppointmentType.objects.get(name=COMMUNITY),
            appt_status=IN_PROGRESS_APPT,
            site=Site.objects.get(id=settings.SITE_ID),
        )

    @tag("1")
    @time_machine.travel(dt.datetime(2019, 5, 11, 8, 00, tzinfo=utc_tz))
    def test_appt_may_not_be_in_community_for_facility_arm(self):
        self.update_appt_1000()
        appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code="1010"
        )
        self.assertEqual(
            get_assignment_for_subject(appointment.subject_identifier), FACILITY_ARM
        )
        traveller = time_machine.travel(appointment.appt_datetime + relativedelta(days=3))
        traveller.start()

        data = self.get_default_appt_data(appointment)
        data.update(
            appt_status=IN_PROGRESS_APPT,
            appt_type=AppointmentType.objects.get(name=COMMUNITY),
        )
        form = AppointmentForm(data=data, instance=appointment)
        form.is_valid()
        self.assertIn("appt_type", form._errors)
        self.assertIn(
            " A facility-based participant may not attend in the community",
            str(form._errors.get("appt_type")),
        )

    @time_machine.travel(dt.datetime(2019, 5, 11, 8, 00, tzinfo=utc_tz))
    def test_appt_may_be_skipped_in_facility_arm2(self):
        self.update_appt_1000()
        appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code="1010"
        )
        self.assertEqual(
            get_assignment_for_subject(appointment.subject_identifier), FACILITY_ARM
        )
        traveller = time_machine.travel(appointment.appt_datetime + relativedelta(days=3))
        traveller.start()

        data = self.get_default_appt_data(appointment)
        data.update(
            appt_status=SKIPPED_APPT,
            appt_type=AppointmentType.objects.get(name=NOT_APPLICABLE),
            appt_timing=NOT_APPLICABLE,
        )
        form = AppointmentForm(data=data, instance=appointment)
        form.is_valid()
        self.assertEqual({}, form._errors)
