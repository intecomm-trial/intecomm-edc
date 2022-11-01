from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields import audit_fieldset_tuple
from edc_constants.constants import UNKNOWN
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.modeladmin_mixins import SiteModelAdminMixin

from ..admin_site import intecomm_screening_admin
from ..forms import PatientLogForm
from ..models import PatientGroup, PatientLog
from .list_filters import InPatientGroup, NextApptListFilter


@admin.register(PatientLog, site=intecomm_screening_admin)
class PatientLogAdmin(
    SiteModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    form = PatientLogForm
    list_per_page = 20
    show_object_tools = True
    autocomplete_fields = ["patient_group"]

    additional_instructions = (
        "Only include patients that are known to have a qualifying "
        "condition and are stable in-care."
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "report_datetime",
                    "site",
                )
            },
        ),
        (
            "Name and contact",
            {
                "fields": (
                    "name",
                    "initials",
                    "hf_identifier",
                )
            },
        ),
        (
            "Contact",
            {
                "fields": (
                    "contact_number",
                    "alt_contact_number",
                    "may_contact",
                )
            },
        ),
        (
            "Address / Location",
            {
                "fields": (
                    "location_description",
                    "patient_group",
                )
            },
        ),
        (
            "Health",
            {
                "description": "Select one or more conditions with a documented diagnoses",
                "fields": (
                    "conditions",
                    "stable",
                ),
            },
        ),
        (
            "Appointments",
            {
                "fields": (
                    "last_routine_appt_date",
                    "next_routine_appt_date",
                )
            },
        ),
        (
            "Health talks",
            {
                "fields": (
                    "first_health_talk",
                    "first_health_talk_date",
                    "second_health_talk",
                    "second_health_talk_date",
                )
            },
        ),
        (
            "Screening and Consent",
            {
                "classes": ("collapse",),
                "fields": ("screening_identifier", "screening_datetime", "subject_identifier"),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "patient",
        "hf_id",
        "group_name",
        "date_logged",
        "next_appt",
        "last_appt",
        "contact",
        "ht1",
        "ht2",
        "site_name",
        "user_created",
        "created",
        "modified",
        "screening_identifier",
        "subject_identifier",
    )

    list_filter = (
        "report_datetime",
        InPatientGroup,
        "stable",
        NextApptListFilter,
        "last_routine_appt_date",
        "first_health_talk",
        "second_health_talk",
        "site",
    )

    filter_horizontal = ("conditions",)

    search_fields = (
        "screening_identifier",
        "subject_identifier",
        "patient_group__name",
        "hf_identifier__exact",
        "initials__exact",
        "name__exact",
        "contact_number__exact",
        "alt_contact_number__exact",
    )

    radio_fields = {
        "stable": admin.VERTICAL,
        "may_contact": admin.VERTICAL,
        "first_health_talk": admin.VERTICAL,
        "second_health_talk": admin.VERTICAL,
    }

    readonly_fields = ("screening_identifier", "screening_datetime", "subject_identifier")

    def post_url_on_delete_kwargs(self, request, obj):
        return {}

    @admin.display(description="Date logged", ordering="report_datetime")
    def date_logged(self, obj=None):
        return obj.report_datetime.date()

    @admin.display(description="next_appt", ordering="next_routine_appt_date")
    def next_appt(self, obj=None):
        return obj.next_routine_appt_date

    @admin.display(description="last_appt", ordering="last_routine_appt_date")
    def last_appt(self, obj=None):
        return obj.last_routine_appt_date

    @admin.display(description="HF ID", ordering="hf_identifier")
    def hf_id(self, obj=None):
        return obj.hf_identifier

    @admin.display(description="Contact", ordering="contact_number")
    def contact(self, obj=None):
        context = dict(
            contact_number=obj.contact_number,
            alt_contact_number=obj.alt_contact_number,
        )
        return format_html(
            render_to_string("intecomm_screening/change_list_contacts.html", context=context)
        )

    @admin.display(description="1st HT", ordering="first_health_talk")
    def ht1(self, obj=None):
        return "?" if obj.first_health_talk == UNKNOWN else obj.first_health_talk

    @admin.display(description="2nd HT", ordering="second_health_talk")
    def ht2(self, obj=None):
        return "?" if obj.second_health_talk == UNKNOWN else obj.second_health_talk

    @admin.display(description="Site", ordering="site")
    def site_name(self, obj=None):
        return obj.site.name.title()

    @admin.display(description="Patient", ordering="name")
    def patient(self, obj=None):
        return f"{obj.name} ({obj.initials})"

    @admin.display(description="Group", ordering="patient_group__name")
    def group_name(self, obj=None):
        if obj.patient_group:
            url = reverse(
                "intecomm_screening_admin:intecomm_screening_patientgroup_changelist"
            )
            url = f"{url}?q={obj.patient_group.name}"
            return format_html(f'<a href="{url}">{obj.patient_group}</a>')
        return "<available>"

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        try:
            patient_group = PatientGroup.objects.get(name=search_term)
        except ObjectDoesNotExist:
            pass
        else:
            queryset |= self.model.objects.filter(
                id__in=[o.id for o in patient_group.patients.all()]
            )
        return queryset, may_have_duplicates
