from __future__ import annotations

from django.contrib.admin import DateFieldListFilter, SimpleListFilter
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from edc_constants.constants import NO, YES
from edc_model_admin.list_filters import FutureDateListFilter


class NextApptListFilter(FutureDateListFilter):
    title = _("Next Appt")

    parameter_name = "next_routine_appt_date"
    field_name = "next_routine_appt_date"


class LastApptListFilter(DateFieldListFilter):
    title = _("Last Appt")

    parameter_name = "last_routine_appt_date"
    field_name = "last_routine_appt_date"


class InPatientGroup(SimpleListFilter):
    title = "In a group"

    parameter_name = "patient_group"
    field_name = "patient_group"

    def lookups(self, request, model_admin) -> tuple:
        return (
            (YES, "Yes"),
            (NO, "No"),
        )

    def queryset(self, request, queryset) -> QuerySet | None:
        qs = None
        if self.value() == YES:
            qs = queryset.filter(patient_group__isnull=False)
        if self.value() == NO:
            qs = queryset.filter(patient_group__isnull=True)
        return qs
