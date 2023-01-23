from __future__ import annotations

from django.contrib.admin import SimpleListFilter
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from edc_constants.constants import DM, HIV, HTN, NCD, NO, TBD, YES
from edc_model_admin.list_filters import FutureDateListFilter, PastDateListFilter
from edc_protocol import Protocol

HIV_ONLY = "HIV_ONLY"
NCD_ONLY = "NCD_ONLY"
HTN_ONLY = "HTN_ONLY"
DM_ONLY = "DM_ONLY"


class NextApptListFilter(FutureDateListFilter):
    title = _("Next Appt")

    parameter_name = "next_appt_date"
    field_name = "next_appt_date"


class LastApptListFilter(PastDateListFilter):
    title = _("Last Appt")

    parameter_name = "last_appt_date"
    field_name = "last_appt_date"


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
            qs = queryset.filter(patientgroup__isnull=False)
        if self.value() == NO:
            qs = queryset.filter(patientgroup__isnull=True)
        return qs


class StableListFilter(SimpleListFilter):
    title = "Stable"

    parameter_name = "stable"
    field_name = "stable"

    def lookups(self, request, model_admin) -> tuple:
        return (
            (YES, "Yes"),
            (NO, "No"),
            (TBD, "To be determined (TBD)"),
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

    parameter_name = "screening_identifier"
    field_name = "screening_identifier"

    def lookups(self, request, model_admin) -> tuple:
        return (
            (YES, "Yes"),
            (NO, "No"),
        )

    def queryset(self, request, queryset) -> QuerySet | None:
        qs = None
        if self.value() == YES:
            qs = queryset.filter(subjectscreening__screening_identifier__isnull=False)
        if self.value() == NO:
            qs = queryset.filter(subjectscreening__screening_identifier__isnull=True)
        return qs


class ConsentedListFilter(SimpleListFilter):
    title = "Consented"

    parameter_name = "subject_identifier"
    field_name = "subject_identifier"

    def lookups(self, request, model_admin) -> tuple:
        return (
            (YES, "Yes"),
            (NO, "No"),
        )

    def queryset(self, request, queryset) -> QuerySet | None:
        qs = None
        if self.value() == YES:
            qs = queryset.filter(
                subjectscreening__subject_identifier__isnull=False,
                subjectscreening__subject_identifier__startswith=Protocol().protocol_number,
            )
        if self.value() == NO:
            qs = queryset.filter(subjectscreening__subject_identifier__isnull=True)
        return qs


class DxListFilter(SimpleListFilter):
    title = "DX"

    parameter_name = "conditions"
    field_name = "conditions"

    def lookups(self, request, model_admin) -> tuple:
        return (
            (NCD, "NCD"),
            (HIV, "HIV"),
            (NCD_ONLY, "NCD only"),
            (DM_ONLY, "DM only"),
            (HIV_ONLY, "HIV only"),
            (HTN_ONLY, "HTN only"),
        )

    def queryset(self, request, queryset) -> QuerySet | None:
        qs = None
        if self.value() == NCD:
            qs = queryset.filter(conditions__name__in=[DM, HTN])
        if self.value() == HIV:
            qs = queryset.filter(conditions__name__in=[HIV])
        if self.value() == NCD_ONLY:
            qs = queryset.filter(conditions__name__in=[DM, HTN]).exclude(
                conditions__name__in=[HIV]
            )
        if self.value() == HIV_ONLY:
            qs = queryset.filter(conditions__name__in=[HIV]).exclude(
                conditions__name__in=[HTN, DM]
            )
        if self.value() == HTN_ONLY:
            qs = queryset.filter(conditions__name__in=[HTN]).exclude(
                conditions__name__in=[HIV, DM]
            )
        if self.value() == DM_ONLY:
            qs = queryset.filter(conditions__name__in=[DM]).exclude(
                conditions__name__in=[HIV, HTN]
            )
        return qs


class AttendDateListFilter(FutureDateListFilter):
    title = "Next Appt"

    parameter_name = "next_appt_date"
    field_name = "patientcall__next_appt_date"

    def queryset(self, request, queryset) -> QuerySet | None:
        qs = super().queryset(request, queryset)
        if qs:
            # dedup
            pk_set = set([obj.pk for obj in qs])
            return qs.model.objects.filter(pk__in=pk_set)
        return qs
