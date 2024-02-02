from django.contrib.admin import SimpleListFilter
from django.db.models import Count, QuerySet
from edc_constants.choices import YES_NO_PENDING_NA
from edc_constants.constants import NO, NOT_APPLICABLE, PENDING, YES
from edc_sites.site import sites

from intecomm_group.models import PatientGroup


class PatientGroupListFilter(SimpleListFilter):
    title = "Group"
    parameter_name = "subject_identifier"

    def lookups(self, request, model_admin):
        site_ids = sites.get_view_only_site_ids_for_user(request=request)
        group_names = [
            (dct["name"], dct["name"].title())
            for dct in PatientGroup.objects.filter(randomized=True, site__in=site_ids)
            .values("name")
            .annotate(count=Count("name"))
        ]
        return tuple(group_names)

    def queryset(self, request, queryset):
        if self.value() and self.value() != "none":
            appt_subject_identifiers = [
                dct["subject_identifier"]
                for dct in queryset.values("subject_identifier").annotate(
                    count=Count("subject_identifier")
                )
            ]
            subject_identifiers = [
                dct["patients__subject_identifier"]
                for dct in PatientGroup.objects.filter(name=self.value())
                .values("patients__subject_identifier")
                .annotate(count=Count("patients__subject_identifier"))
            ]
            subject_identifiers = [
                v for v in subject_identifiers if v in appt_subject_identifiers
            ]
            queryset = queryset.filter(subject_identifier__in=subject_identifiers)
        return queryset


class VlStatusListFilter(SimpleListFilter):
    title = "VL Resulted"

    parameter_name = "vl_resulted"
    field_name = "has_vl"

    def lookups(self, request, model_admin) -> tuple:
        return YES_NO_PENDING_NA

    def queryset(self, request, queryset) -> QuerySet | None:
        qs = None
        if self.value() == YES:
            qs = queryset.filter(has_vl=YES)
        if self.value() == NO:
            qs = queryset.filter(has_vl=NO)
        if self.value() == PENDING:
            qs = queryset.filter(has_vl=PENDING)
        if self.value() == NOT_APPLICABLE:
            qs = queryset.filter(has_vl=NOT_APPLICABLE)
        return qs
