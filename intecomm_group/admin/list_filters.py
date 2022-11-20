from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from edc_model_admin.list_filters import FutureDateListFilter


class PatientGroupApptListFilter(FutureDateListFilter):
    title = _("Appt")

    parameter_name = "appt_datetime"
    field_name = "appt_datetime"
