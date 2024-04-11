from django.contrib.auth.models import Permission, User
from django.contrib.sites.models import Site
from django.test import override_settings
from django.urls import reverse
from django_webtest import WebTest
from edc_dashboard.url_names import url_names

from intecomm_dashboard.views import SubjectDashboardView
from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin
from intecomm_subject.models import DrugSupplyDm, DrugSupplyHiv, DrugSupplyHtn
from intecomm_subject.models import HealthEconomics as OldHealthEconomics


class TestSubjectDashboard(IntecommTestCaseMixin, WebTest):
    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create_superuser("user_login", "u@example.com", "pass")
        self.user.is_active = True
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.user.refresh_from_db()
        self.exclude_models = [
            DrugSupplyDm,
            DrugSupplyHtn,
            DrugSupplyHiv,
            OldHealthEconomics,
        ]
        self.user.userprofile.sites.add(Site.objects.get(id=101))
        self.user.userprofile.sites.add(Site.objects.get(id=201))
        self.user.user_permissions.add(Permission.objects.get(codename="view_appointment"))

    def login(self):
        form = None
        response = self.app.get(reverse("admin:index")).maybe_follow()
        for index, form in response.forms.items():
            if form.action == "/i18n/setlang/":
                # exclude the locale form
                continue
            else:
                break
        form["username"] = self.user.username
        form["password"] = "pass"  # nosec B105
        return form.submit()

    @override_settings(SITE_ID=201)
    def test_dashboard_ok(self):
        subject_screening = self.get_subject_screening()
        self.assertEqual(subject_screening.reasons_ineligible, None)
        self.assertTrue(subject_screening.eligible)

        subject_consent = self.get_subject_consent(subject_screening)
        self.assertIsNotNone(subject_consent.subject_identifier)

        self.login()

        url_name = url_names.get(SubjectDashboardView.dashboard_url_name)
        url = reverse(
            url_name, kwargs=dict(subject_identifier=subject_consent.subject_identifier)
        )
        self.app.get(url, user=self.user, status=200)

    @override_settings(SITE_ID=101)
    def test_dashboard_ug_ok(self):
        subject_screening = self.get_subject_screening()
        self.assertEqual(subject_screening.reasons_ineligible, None)
        self.assertTrue(subject_screening.eligible)

        subject_consent = self.get_subject_consent(subject_screening)
        self.assertIsNotNone(subject_consent.subject_identifier)

        self.login()

        url_name = url_names.get(SubjectDashboardView.dashboard_url_name)
        url = reverse(
            url_name, kwargs=dict(subject_identifier=subject_consent.subject_identifier)
        )
        self.app.get(url, user=self.user, status=200)
