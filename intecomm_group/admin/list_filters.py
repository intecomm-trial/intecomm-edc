from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from edc_model_admin.list_filters import FutureDateListFilter, PastDateListFilter


class PatientGroupApptListFilter(FutureDateListFilter):
    title = _("Appt")

    parameter_name = "appt_datetime"
    field_name = "appt_datetime"


class PatientGroupLastCallListFilter(PastDateListFilter):
    title = _("Last call")

    parameter_name = "report_datetime"
    field_name = "report_datetime"
