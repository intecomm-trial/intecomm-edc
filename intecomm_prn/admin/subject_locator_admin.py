from __future__ import annotations

from django.contrib import admin
from django.template.loader import render_to_string
from edc_locator.admin_site import edc_locator_admin
from edc_locator.modeladmin_mixins import SubjectLocatorModelAdminMixin
from edc_locator.models import SubjectLocator as DefaultSubjectLocator
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from intecomm_prn.admin_site import intecomm_prn_admin
from intecomm_prn.forms import SubjectLocatorForm
from intecomm_prn.models import SubjectLocator
from intecomm_screening.models import PatientLog

edc_locator_admin.unregister(DefaultSubjectLocator)


@admin.register(SubjectLocator, site=intecomm_prn_admin)
class SubjectLocatorAdmin(
    SubjectLocatorModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    list_per_page = 5

    form = SubjectLocatorForm

    @admin.display(description="Contacts")
    def contacts(self, obj):
        patient_log = PatientLog.objects.get(subject_identifier=obj.subject_identifier)
        context = dict(
            patient_log=patient_log,
            subject_cell=obj.subject_cell,
            subject_cell_alt=obj.subject_cell_alt,
            subject_phone=obj.subject_phone,
            subject_phone_alt=obj.subject_phone_alt,
        )
        return render_to_string(
            "intecomm_prn/changelist_locator_contacts.html", context=context
        )
