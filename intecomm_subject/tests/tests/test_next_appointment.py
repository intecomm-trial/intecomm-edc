from unittest.mock import patch

import django.conf.locale
from django.contrib.auth.models import User
from django.urls import reverse
from django_webtest import WebTest
from edc_constants.internationalization import EXTRA_LANG_INFO


@patch.dict(
    # Add custom languages not provided by Django
    "django.conf.locale.LANG_INFO",
    dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO),
)
class TestNextAppointment(WebTest):
    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create_superuser("user_login", "u@example.com", "pass")
        self.user.is_active = True
        self.user.is_staff = True
        self.user.save()
        self.user.refresh_from_db()

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

    def test_admin_ok(self):
        self.login()
