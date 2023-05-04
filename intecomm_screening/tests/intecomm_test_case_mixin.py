from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.sites.models import Site
from edc_appointment.constants import IN_PROGRESS_APPT, INCOMPLETE_APPT
from edc_appointment.tests.appointment_test_case_mixin import AppointmentTestCaseMixin
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays
from edc_list_data.site_list_data import site_list_data
from edc_metadata import REQUIRED
from edc_metadata.models import CrfMetadata
from edc_randomization.site_randomizers import site_randomizers
from edc_sites import add_or_update_django_sites, get_sites_by_country
from edc_visit_schedule.constants import DAY1
from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_bakery import baker

from intecomm_sites.sites import fqdn
from intecomm_sites.tests.site_test_case_mixin import SiteTestCaseMixin
from intecomm_subject.models import SubjectVisit

from ..models import SubjectScreening

fake = Faker()
now = datetime(2019, 5, 1).astimezone(ZoneInfo("UTC"))
tomorrow = now + relativedelta(days=1)


class IntecommTestCaseMixin(AppointmentTestCaseMixin, SiteTestCaseMixin):
    fqdn = fqdn

    default_sites = get_sites_by_country("tanzania")

    site_names = [s.name for s in default_sites]

    import_randomization_list = True

    sid_count_for_tests = 5

    @classmethod
    def setUpTestData(cls):
        import_holidays(test=True)
        add_or_update_django_sites(sites=get_sites_by_country("tanzania"))
        if cls.import_randomization_list:
            randomizer_cls = site_randomizers.get("default")
            randomizer_cls.import_list(
                verbose=False, sid_count_for_tests=cls.sid_count_for_tests
            )
        site_list_data.initialize()
        site_list_data.autodiscover()

    def get_subject_screening(
        self,
        report_datetime: datetime | None = None,
        eligibility_datetime: datetime | None = None,
        gender: str | None = None,
        ethnicity: str | None = None,
        age_in_years: int | None = None,
    ):
        eligible_options = {}
        if report_datetime:
            eligible_options.update(report_datetime=report_datetime)
        eligible_options["age_in_years"] = age_in_years or eligible_options["age_in_years"]
        eligible_options["gender"] = gender or eligible_options["gender"]
        eligible_options["ethnicity"] = ethnicity or eligible_options["ethnicity"]
        subject_screening = SubjectScreening.objects.create(
            user_created="erikvw",
            user_modified="erikvw",
            **eligible_options,
        )
        screening_identifier = subject_screening.screening_identifier
        self.assertEqual(subject_screening.reasons_ineligible, None)
        self.assertEqual(subject_screening.eligible, YES)

        subject_screening = SubjectScreening.objects.get(
            screening_identifier=screening_identifier
        )

        self.assertTrue(subject_screening.eligible)

        if eligibility_datetime:
            subject_screening.eligibility_datetime = eligibility_datetime
            subject_screening.save()
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=screening_identifier
            )
        return subject_screening

    @staticmethod
    def get_subject_consent(subject_screening, consent_datetime=None, site_id=None):
        return baker.make_recipe(
            "intecomm_consent.subjectconsent",
            user_created="erikvw",
            user_modified="erikvw",
            screening_identifier=subject_screening.screening_identifier,
            initials=subject_screening.initials,
            gender=subject_screening.gender,
            dob=(now.date() - relativedelta(years=subject_screening.age_in_years)),
            site=Site.objects.get(id=site_id or settings.SITE_ID),
            consent_datetime=consent_datetime or subject_screening.report_datetime,
        )

    def get_subject_visit(
        self,
        visit_code: str | None = None,
        visit_code_sequence: int | None = None,
        subject_screening=None,
        subject_consent=None,
        reason: str | None = None,
        appt_datetime: datetime | None = None,
        gender: str | None = None,
        ethnicity: str | None = None,
        age_in_years: int | None = None,
        screening_datetime: datetime | None = None,
        eligibility_datetime: datetime | None = None,
    ):
        reason = reason or SCHEDULED
        subject_screening = subject_screening or self.get_subject_screening(
            gender=gender,
            ethnicity=ethnicity,
            age_in_years=age_in_years,
            report_datetime=screening_datetime,
            eligibility_datetime=eligibility_datetime,
        )
        subject_consent = subject_consent or self.get_subject_consent(subject_screening)
        options = dict(
            subject_identifier=subject_consent.subject_identifier,
            visit_code=visit_code or DAY1,
            visit_code_sequence=(
                visit_code_sequence if visit_code_sequence is not None else 0
            ),
            reason=reason,
        )
        if appt_datetime:
            options.update(appt_datetime=appt_datetime)
        appointment = self.get_appointment(**options)
        subject_visit = SubjectVisit(
            appointment=appointment,
            reason=SCHEDULED,
            report_datetime=appointment.appt_datetime,
        )
        subject_visit.save()
        subject_visit.refresh_from_db()
        return subject_visit

    @staticmethod
    def get_next_subject_visit(subject_visit):
        appointment = subject_visit.appointment
        appointment.appt_status = INCOMPLETE_APPT
        appointment.save()
        appointment.refresh_from_db()
        next_appointment = appointment.next_by_timepoint
        next_appointment.appt_status = IN_PROGRESS_APPT
        next_appointment.save()
        subject_visit = SubjectVisit(
            appointment=next_appointment,
            reason=SCHEDULED,
            report_datetime=next_appointment.appt_datetime,
            visit_code=next_appointment.visit_code,
            visit_code_sequence=next_appointment.visit_code_sequence,
        )
        subject_visit.save()
        subject_visit.refresh_from_db()
        return subject_visit

    @staticmethod
    def get_crf_metadata(subject_visit):
        return CrfMetadata.objects.filter(
            subject_identifier=subject_visit.subject_identifier,
            visit_code=subject_visit.visit_code,
            visit_code_sequence=subject_visit.visit_code_sequence,
            entry_status=REQUIRED,
        )
