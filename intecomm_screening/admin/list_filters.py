from __future__ import annotations

from django.contrib.admin import DateFieldListFilter
from django.utils.translation import gettext_lazy as _
from edc_model_admin.list_filters import FutureDateListFilter


class NextApptListFilter(FutureDateListFilter):
    title = _("Next Appt")

    parameter_name = "next_routine_appt_date"
    field_name = "next_routine_appt_date"


class LastApptListFilter(DateFieldListFilter):
    title = _("Last Appt")

    parameter_name = "last_routine_appt_date"
    field_name = "last_routine_appt_date"
