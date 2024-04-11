from django.test import override_settings
from django.urls import reverse
from django_webtest import WebTest
from edc_dashboard.url_names import url_names
from edc_test_utils.get_user_for_tests import get_user_for_tests

from intecomm_dashboard.views import (
    AeListboardView,
    DeathReportListboardView,
    ScreenGroupListboardView,
    SubjectListboardView,
)
from intecomm_subject.models import DrugSupplyDm, DrugSupplyHiv, DrugSupplyHtn
from intecomm_subject.models import HealthEconomics as OldHealthEconomics


class TestViews(WebTest):
    def setUp(self) -> None:
        super().setUp()
        self.user = get_user_for_tests()
        self.user.is_superuser = True
        self.user.save()
        self.user.refresh_from_db()
        self.exclude_models = [
            DrugSupplyDm,
            DrugSupplyHtn,
            DrugSupplyHiv,
            OldHealthEconomics,
        ]

    def login(self):
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

    @override_settings(SITE_ID=101)
    def test_listboards_ok(self):
        self.login()

        url_name = url_names.get(ScreenGroupListboardView.listboard_url)
        url = reverse(url_name)
        response = self.app.get(url, user=self.user, status=200)
        self.assertIn(ScreenGroupListboardView.listboard_panel_title, response.text)

        url_name = url_names.get(AeListboardView.listboard_url)
        url = reverse(url_name)
        response = self.app.get(url, user=self.user, status=200)
        self.assertIn(AeListboardView.listboard_panel_title, response.text)

        url_name = url_names.get(SubjectListboardView.listboard_url)
        url = reverse(url_name)
        response = self.app.get(url, user=self.user, status=200)
        self.assertIn(SubjectListboardView.listboard_panel_title, response.text)

        url_name = url_names.get(DeathReportListboardView.listboard_url)
        url = reverse(url_name)
        response = self.app.get(url, user=self.user, status=200)
        self.assertIn(DeathReportListboardView.listboard_panel_title, response.text)
