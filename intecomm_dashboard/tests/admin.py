from django.contrib.admin import AdminSite as DjangoAdminSite
from edc_locator.models import SubjectLocator

from intecomm_consent.models import SubjectConsent
from intecomm_screening.models import SubjectScreening
from intecomm_subject.models import SubjectRequisition, SubjectVisit


class AdminSite(DjangoAdminSite):
    site_title = "Intecomm Subject"
    site_header = "Intecomm Subject"
    index_title = "Intecomm Subject"
    site_url = "/administration/"


intecomm_test_admin = AdminSite(name="intecomm_test_admin")

intecomm_test_admin.register(SubjectScreening)
intecomm_test_admin.register(SubjectConsent)
intecomm_test_admin.register(SubjectLocator)
intecomm_test_admin.register(SubjectVisit)
intecomm_test_admin.register(SubjectRequisition)
