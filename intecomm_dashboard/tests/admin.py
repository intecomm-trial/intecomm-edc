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


meta_test_admin = AdminSite(name="intecomm_test_admin")

meta_test_admin.register(SubjectScreening)
meta_test_admin.register(SubjectConsent)
meta_test_admin.register(SubjectLocator)
meta_test_admin.register(SubjectVisit)
meta_test_admin.register(SubjectRequisition)
