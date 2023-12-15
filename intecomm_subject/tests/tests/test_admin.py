from django.apps import apps as django_apps
from django.contrib.auth.models import Permission, User
from django.contrib.sites.models import Site
from django.test import override_settings
from django.urls import NoReverseMatch, reverse
from django_webtest import WebTest

from intecomm_subject.models import DrugSupplyDm, DrugSupplyHiv, DrugSupplyHtn
from intecomm_subject.models import HealthEconomics as OldHealthEconomics


class TestAdmin(WebTest):
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
    def test_admin_changelists_ok(self):
        self.login()
        app_config = django_apps.get_app_config("intecomm_subject")
        models = [
            model for model in app_config.get_models() if model not in self.exclude_models
        ]
        urls = []
        errors = []
        for model in models:
            app_name, model_name = model._meta.label_lower.split(".")
            if "historical" not in model_name:
                url_name = f"{app_name}_admin:{app_name}_{model_name}_changelist"
                try:
                    url = reverse(url_name)
                except NoReverseMatch:
                    errors.append(url_name)
                else:
                    urls.append((url, model))
        if errors:
            as_str = "\n".join(errors)
            self.fail(f"NoReverseMatch unexpectedly raised. Got urls \n{as_str}.")
        for url, model in urls:
            response = self.app.get(url, user=self.user, status=200)
            print(model._meta.verbose_name_plural)
            self.assertTrue(
                str(model._meta.verbose_name_plural) in response.text,
                msg=f"{model._meta.verbose_name_plural} not found in changelist html",
            )
