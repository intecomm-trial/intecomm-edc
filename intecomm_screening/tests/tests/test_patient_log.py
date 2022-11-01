from django.test import TestCase, override_settings, tag
from edc_utils import get_utcnow
from faker import Faker

from intecomm_screening.forms import PatientLogForm

fake = Faker()


@override_settings(SITE_ID=101)
class TestPatientLog(TestCase):
    def get_data(self) -> dict:
        name = fake.name()
        return dict(
            report_datetime=get_utcnow(),
            site=101,
            name=name,
            initials=f"{name[0]}X",
            contact_number="765456",
        )

    @tag("1")
    def test_add_patient_log(self):
        data = self.get_data()
        form = PatientLogForm(data=data)
        form.is_valid()
        self.assertEqual({}, form._errors)
