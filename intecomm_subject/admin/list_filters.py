from django.contrib.admin import SimpleListFilter
from django.db.models import Count
from edc_sites.permissions import get_view_only_sites_for_user

from intecomm_group.models import PatientGroup


class PatientGroupListFilter(SimpleListFilter):
    title = "Group"
    parameter_name = "subject_identifier"

    def lookups(self, request, model_admin):
        site_ids = get_view_only_sites_for_user(request.user, request.site.id, request=request)
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
