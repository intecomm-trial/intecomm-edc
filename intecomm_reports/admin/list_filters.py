from django.contrib.admin import SimpleListFilter
from edc_visit_schedule.admin import (
    ScheduleStatusListFilter as BaseScheduleStatusListFilter,
)
from edc_visit_schedule.models import SubjectScheduleHistory


class VlListFilter(SimpleListFilter):
    title = "VL"
    parameter_name = "vl_value"

    def lookups(self, request, model_admin):
        return (
            ("missing", "Missing"),
            ("not_missing", "Not missing"),
        )

    def queryset(self, request, queryset):
        if self.value() != "none":
            if self.value() == "missing":
                queryset = queryset.filter(**{f"{self.parameter_name}__isnull": True})
            elif self.value() == "not_missing":
                queryset = queryset.filter(**{f"{self.parameter_name}__isnull": False})
        return queryset


class BaselineVlListFilter(VlListFilter):
    title = "Baseline VL"
    parameter_name = "baseline_vl"


class EndlineVlListFilter(VlListFilter):
    title = "Baseline VL"
    parameter_name = "endline_vl"


class ScheduleStatusListFilter(BaseScheduleStatusListFilter):
    def lookups(self, request, model_admin):
        return ("on", "On schedule"), ("off", "Off schedule")

    @property
    def subject_identifiers(self):
        return SubjectScheduleHistory.objects.filter(
            offschedule_datetime__isnull=self.value() == "on"
        ).values_list("subject_identifier", flat=True)
