from __future__ import annotations

from django.contrib.admin import SimpleListFilter
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from edc_constants.constants import DM, HIV, HTN, NCD, NO, TBD, YES
from edc_model_admin.list_filters import FutureDateListFilter, PastDateListFilter


class NextApptListFilter(FutureDateListFilter):
    title = _("Next Appt")

    parameter_name = "next_routine_appt_date"
    field_name = "next_routine_appt_date"


class LastApptListFilter(PastDateListFilter):
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


class StableListFilter(SimpleListFilter):
    title = "Stable"

    parameter_name = "stable"
    field_name = "stable"

    def lookups(self, request, model_admin) -> tuple:
        return (
            (YES, "Yes"),
            (NO, "No"),
            (TBD, "To be determined"),
        )

    def queryset(self, request, queryset) -> QuerySet | None:
        qs = None
        if self.value() == YES:
            qs = queryset.filter(stable=YES)
        if self.value() == NO:
            qs = queryset.filter(stable=NO)
        if self.value() == TBD:
            qs = queryset.filter(stable=TBD)
        return qs


class ScreenedListFilter(SimpleListFilter):
    title = "Screened"

    parameter_name = "screening_datetime"
    field_name = "screening_datetime"

    def lookups(self, request, model_admin) -> tuple:
        return (
            (YES, "Yes"),
            (NO, "No"),
        )

    def queryset(self, request, queryset) -> QuerySet | None:
        qs = None
        if self.value() == YES:
            qs = queryset.filter(screening_datetime__isnull=False)
        if self.value() == NO:
            qs = queryset.filter(screening_datetime__isnull=True)
        return qs


class ConsentedListFilter(SimpleListFilter):
    title = "Consented"

    parameter_name = "consent_datetime"
    field_name = "consent_datetime"

    def lookups(self, request, model_admin) -> tuple:
        return (
            (YES, "Yes"),
            (NO, "No"),
        )

    def queryset(self, request, queryset) -> QuerySet | None:
        qs = None
        if self.value() == YES:
            qs = queryset.filter(consent_datetime__isnull=False)
        if self.value() == NO:
            qs = queryset.filter(consent_datetime__isnull=True)
        return qs


class DxListFilter(SimpleListFilter):
    title = "DX"

    parameter_name = "conditions"
    field_name = "conditions"

    def lookups(self, request, model_admin) -> tuple:
        return (
            (NCD, "NCD"),
            (HIV, "HIV"),
        )

    def queryset(self, request, queryset) -> QuerySet | None:
        qs = None
        if self.value() == NCD:
            qs = queryset.filter(conditions__name__in=[DM, HTN])
        if self.value() == HIV:
            qs = queryset.filter(conditions__name__in=[HIV])
        return qs
