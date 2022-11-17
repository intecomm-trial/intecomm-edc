from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.modeladmin_mixins import SiteModelAdminMixin

from intecomm_screening.admin.list_filters import InPatientGroup

from ..admin_site import intecomm_group_admin
from ..forms import PatientLogForm
from ..models import PatientLog

# from .patient_call_inlines import AddPatientCallInline, ViewPatientCallInline


@admin.register(PatientLog, site=intecomm_group_admin)
class PatientLogAdmin(
    SiteModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    form = PatientLogForm
    list_per_page = 20
    show_object_tools = True
    change_list_template: str = "intecomm_group/admin/patientlog_change_list.html"

    # inlines = [AddPatientCallInline, ViewPatientCallInline]

    additional_instructions = format_html(
        '<h3 style="color:orange;">Note:</h3> Log calls and call attempts at the bottom '
        "of this form."
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
                    "gender",
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
            "Screening and Consent",
            {
                "classes": ("collapse",),
                "fields": (
                    "screening_identifier",
                    "screening_datetime",
                    "subject_identifier",
                    "consent_datetime",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "patient",
        "subject_identifier",
        "group_name",
        "contacts",
        "site_name",
        "user_created",
        "created",
        "modified",
        "screening_identifier",
    )

    list_filter = (
        "report_datetime",
        "call_attempts",
        InPatientGroup,
        "gender",
    )

    search_fields = (
        "id",
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
        "gender": admin.VERTICAL,
    }

    readonly_fields = (
        "screening_identifier",
        "screening_datetime",
        "subject_identifier",
        "consent_datetime",
    )

    def post_url_on_delete_kwargs(self, request, obj):
        return {}

    @admin.display(description="Contacts", ordering="contact_number")
    def contacts(self, obj=None):
        add_patient_call_url = reverse(
            "intecomm_screening_admin:intecomm_screening_patientcall_add"
        )
        patient_call_url = reverse(
            "intecomm_screening_admin:intecomm_screening_patientcall_changelist"
        )
        patient_call_url = f"{patient_call_url}?q={obj.id}"
        context = dict(
            patient_log_id=obj.id,
            add_patient_call_url=add_patient_call_url,
            patient_call_url=patient_call_url,
            contact_number=obj.contact_number,
            alt_contact_number=obj.alt_contact_number,
            call_attempts=obj.call_attempts,
        )
        return format_html(
            render_to_string("intecomm_screening/change_list_contacts.html", context=context)
        )

    @admin.display(description="Site", ordering="site")
    def site_name(self, obj=None):
        return obj.site.name.title()

    @admin.display(description="Patient", ordering="name")
    def patient(self, obj=None):
        return f"{obj.name} ({obj.initials})"

    @admin.display(description="Group", ordering="patient_group__name")
    def group_name(self, obj=None):
        if obj.patient_group:
            url = reverse("intecomm_group_admin:intecomm_group_patientgroup_changelist")
            url = f"{url}?q={obj.patient_group.name}"
            return format_html(f'<a href="{url}">{obj.patient_group}</a>')
        return "<available>"

    @admin.display(description="Calls", ordering="contact_attempts")
    def calls(self, obj):
        url = reverse("intecomm_screening_admin:intecomm_screening_patientcall_changelist")
        url = f"{url}?q={obj.patientcall.id}"
        return format_html(f'<A href="{url}">{obj.contact_attempts}</a>')

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        try:
            patient_log = self.model.objects.get(name=search_term)
        except ObjectDoesNotExist:
            pass
        else:
            queryset |= self.model.objects.filter(id=patient_log.id)
        return queryset, may_have_duplicates
