from django.test import TestCase
from edc_auth.auth_updater.group_updater import GroupUpdater, PermissionsCodenameError

from intecomm_auth.auth_objects import clinic_codenames, screening_codenames


class TestAuths(TestCase):
    def test_auth(self):
        group_updater = GroupUpdater(groups={})
        for codename in clinic_codenames:
            try:
                group_updater.get_from_dotted_codename(codename)
            except PermissionsCodenameError as e:
                self.fail(f"PermissionsCodenameError raised unexpectedly. Got {e}")
        for codename in screening_codenames:
            try:
                group_updater.get_from_dotted_codename(codename)
            except PermissionsCodenameError as e:
                self.fail(f"PermissionsCodenameError raised unexpectedly. Got {e}")
