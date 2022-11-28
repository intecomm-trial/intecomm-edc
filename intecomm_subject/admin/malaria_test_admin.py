from django.contrib import admin
from edc_microscopy.modeladmin_mixins import MalariaTestModelAdminMixin

from ..admin_site import intecomm_subject_admin
from ..forms import MalariaTestForm
from ..models import MalariaTest
from .modeladmin_mixins import CrfModelAdmin


@admin.register(MalariaTest, site=intecomm_subject_admin)
class MalariaTestAdmin(MalariaTestModelAdminMixin, CrfModelAdmin):

    form = MalariaTestForm
