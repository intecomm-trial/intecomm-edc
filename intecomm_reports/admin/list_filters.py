from django.contrib.admin import SimpleListFilter
from edc_model_admin.list_filters import PastDateListFilter
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
    title = "Endline VL"
    parameter_name = "endline_vl"


class ScheduleStatusListFilter(BaseScheduleStatusListFilter):
    def lookups(self, request, model_admin):
        return ("on", "On schedule"), ("off", "Off schedule")

    @property
    def subject_identifiers(self):
        return SubjectScheduleHistory.objects.filter(
            offschedule_datetime__isnull=self.value() == "on"
        ).values_list("subject_identifier", flat=True)


class BaselineVlDateListFilter(PastDateListFilter):
    title = "Baseline VL Date"

    parameter_name = "baseline_vl_date"
    field_name = "baseline_vl_date"


class EndlineVlDateListFilter(PastDateListFilter):
    title = "Endline VL Date"

    parameter_name = "endline_vl_date"
    field_name = "endline_vl_date"


class LastVlDateListFilter(PastDateListFilter):
    title = "Last VL Date"

    parameter_name = "last_vl_date"
    field_name = "last_vl_date"


class NextVlDateListFilter(PastDateListFilter):
    title = "Next VL Date"

    parameter_name = "next_vl_date"
    field_name = "next_vl_date"


class VlDateListFilter(PastDateListFilter):
    title = "VL Date"

    parameter_name = "vl_date"
    field_name = "vl_date"
