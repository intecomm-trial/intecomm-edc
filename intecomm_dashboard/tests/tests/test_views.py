from django.contrib.auth.models import User
from django.urls import reverse
from django_webtest import WebTest
from edc_dashboard import url_names

from intecomm_dashboard.views import (
    AeListboardView,
    CommunitySubjectListboardView,
    DeathReportListboardView,
    FacilitySubjectListboardView,
    ScreenGroupListboardView,
)
from intecomm_subject.models import DrugSupplyDm, DrugSupplyHiv, DrugSupplyHtn
from intecomm_subject.models import HealthEconomics as OldHealthEconomics


class TestViews(WebTest):
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

        url_name = url_names.get(DeathReportListboardView.listboard_url)
        url = reverse(url_name)
        response = self.app.get(url, user=self.user, status=200)
        self.assertIn(DeathReportListboardView.listboard_panel_title, response.text)

        url_name = url_names.get(CommunitySubjectListboardView.listboard_url)
        url = reverse(url_name)
        response = self.app.get(url, user=self.user, status=200)
        self.assertIn(CommunitySubjectListboardView.listboard_panel_title, response.text)

        url_name = url_names.get(FacilitySubjectListboardView.listboard_url)
        url = reverse(url_name)
        response = self.app.get(url, user=self.user, status=200)
        self.assertIn(FacilitySubjectListboardView.listboard_panel_title, response.text)
