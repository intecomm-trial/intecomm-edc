import re
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.contrib.sites.models import Site
from django.test import override_settings
from django.urls import reverse
from django_webtest import WebTest
from edc_constants.constants import HIV, UUID_PATTERN
from edc_test_utils.webtest import login
from model_bakery.baker import make_recipe

from intecomm_lists.models import Conditions

from ..intecomm_test_case_mixin import IntecommTestCaseMixin


class TestScreening(IntecommTestCaseMixin, WebTest):
    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create_superuser("user_login", "u@example.com", "pass")
        self.user.is_active = True
        self.user.is_staff = True
        self.user.save()
        self.user.refresh_from_db()
        self.user.userprofile.sites.add(Site.objects.get(id=101))
        self.user.userprofile.sites.add(Site.objects.get(id=201))
        self.user.user_permissions.add(Permission.objects.get(codename="view_appointment"))

    @override_settings(SITE_ID=201, EDC_CONSENT_REMOVE_PATIENT_NAMES_FROM_COUNTRIES=["uganda"])
    def test_add_patient_log_with_names(self):
        changelist_url_name = (
            "intecomm_screening_admin:intecomm_screening_patientlog_changelist"
        )
        login(self, user=self.user, redirect_url=changelist_url_name)

        changelist_url = reverse(changelist_url_name)
        response = self.app.get(changelist_url, user=self.user)
        add_url = reverse("intecomm_screening_admin:intecomm_screening_patientlog_add")
        self.assertIn(add_url, response.text)
        response = self.app.get(add_url, user=self.user)
        self.assertIn("legal_name", response.text)
        self.assertIn("familiar_name", response.text)

        obj = make_recipe(
            "intecomm_screening.patientlog",
            legal_name="NAMEA AAAA",
            familiar_name="NAMEA AAAA",
            initials="NA",
            hospital_identifier=uuid4().hex,
            contact_number="123456789",
            site_id=settings.SITE_ID,
        )
        obj.conditions.add(Conditions.objects.get(name=HIV))
        obj.refresh_from_db()

        change_url = reverse(
            "intecomm_screening_admin:intecomm_screening_patientlog_change",
            args=(obj.id,),
        )
        response = self.app.get(change_url, user=self.user)
        self.assertIn(str(obj.legal_name), response.text)
        self.assertIn(str(obj.familiar_name), response.text)

    @override_settings(SITE_ID=101)
    def test_add_patient_log_without_names(self):
        changelist_url_name = (
            "intecomm_screening_admin:intecomm_screening_patientlogug_changelist"
        )
        login(self, user=self.user, redirect_url=changelist_url_name)

        changelist_url = reverse(changelist_url_name)
        response = self.app.get(changelist_url, user=self.user)
        add_url = reverse("intecomm_screening_admin:intecomm_screening_patientlogug_add")
        self.assertIn(add_url, response.text)
        response = self.app.get(add_url, user=self.user)
        self.assertNotIn("legal_name", response.text)
        self.assertNotIn("familiar_name", response.text)

        obj = make_recipe(
            "intecomm_screening.patientlogug",
            legal_name=str(uuid4()),
            familiar_name=str(uuid4()),
            initials="BB",
            hospital_identifier=uuid4().hex,
            contact_number="123456780",
            site_id=settings.SITE_ID,
        )
        obj.conditions.add(Conditions.objects.get(name=HIV))

        obj.refresh_from_db()
        self.assertTrue(re.match(UUID_PATTERN, str(obj.legal_name)))
        self.assertTrue(re.match(UUID_PATTERN, str(obj.familiar_name)))

        response = self.app.get(changelist_url, user=self.user)
        self.assertNotIn(str(obj.legal_name), response.text)
        self.assertNotIn(str(obj.familiar_name), response.text)

        change_url = reverse(
            "intecomm_screening_admin:intecomm_screening_patientlogug_change",
            args=(obj.id,),
        )

        response = self.app.get(change_url, user=self.user)
        self.assertNotIn(str(obj.legal_name), response.text)
        self.assertNotIn(str(obj.familiar_name), response.text)

    @override_settings(SITE_ID=201)
    def test_add_patient_log_with_names2(self):
        changelist_url_name = (
            "intecomm_screening_admin:intecomm_screening_patientlog_changelist"
        )
        login(self, user=self.user, redirect_url=changelist_url_name)

        changelist_url = reverse(changelist_url_name)
        response = self.app.get(changelist_url, user=self.user)
        add_url = reverse("intecomm_screening_admin:intecomm_screening_patientlog_add")
        self.assertIn(add_url, response.text)
        response = self.app.get(add_url, user=self.user)
        self.assertIn("legal_name", response.text)
        self.assertIn("familiar_name", response.text)

        obj = make_recipe(
            "intecomm_screening.patientlog",
            legal_name="Tianna Esperanza",
            familiar_name="Tianna Esperanza",
            initials="TE",
            hospital_identifier=uuid4().hex,
            contact_number="123456780",
            site_id=settings.SITE_ID,
        )
        obj.conditions.add(Conditions.objects.get(name=HIV))

        obj.refresh_from_db()

        response = self.app.get(changelist_url, user=self.user)
        self.assertIn(str(obj.legal_name), response.text)
        self.assertIn(str(obj.familiar_name), response.text)

        change_url = reverse(
            "intecomm_screening_admin:intecomm_screening_patientlog_change",
            args=(obj.id,),
        )

        response = self.app.get(change_url, user=self.user)
        self.assertIn(str(obj.legal_name), response.text)
        self.assertIn(str(obj.familiar_name), response.text)

    @override_settings(
        SITE_ID=None,
        EDC_CONSENT_REMOVE_PATIENT_NAMES_FROM_COUNTRIES=["uganda"],
        ALLOWED_HOSTS=["amana.tz.localhost"],
        LANGUAGES=[("en", "English"), ("sw", "Swahili")],
    )
    def test_add_patient_log_with_names_with_site_from_http_host(self):
        site_obj = Site.objects.get(id=201)
        site_obj.domain = "amana.tz.localhost"
        site_obj.save()

        changelist_url_name = (
            "intecomm_screening_admin:intecomm_screening_patientlog_changelist"
        )

        login(
            self,
            user=self.user,
            redirect_url=changelist_url_name,
            extra_environ=dict(HTTP_HOST="amana.tz.localhost"),
        )

        changelist_url = reverse(changelist_url_name)
        response = self.app.get(
            changelist_url,
            user=self.user,
            extra_environ=dict(HTTP_HOST="amana.tz.localhost"),
        )
        add_url = reverse("intecomm_screening_admin:intecomm_screening_patientlog_add")
        self.assertIn(add_url, response.text)
        response = self.app.get(
            add_url,
            user=self.user,
            extra_environ=dict(HTTP_HOST="amana.tz.localhost"),
        )
        self.assertIn("legal_name", response.text)
        self.assertIn("familiar_name", response.text)
