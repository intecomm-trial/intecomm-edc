from django.contrib.auth.models import User
from django.urls import reverse
from django_webtest import WebTest


class TestNextAppointment(WebTest):
    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create_superuser("user_login", "u@example.com", "pass")
        self.user.is_active = True
        self.user.is_staff = True
        self.user.save()
        self.user.refresh_from_db()

    def login(self):
        form = self.app.get(reverse("admin:index")).maybe_follow().form
        form["username"] = self.user.username
        form["password"] = "pass"  # nosec B105
        return form.submit()

    def test_admin_ok(self):
        self.login()
