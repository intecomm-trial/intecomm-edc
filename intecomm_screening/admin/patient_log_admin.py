from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.modeladmin_mixins import SiteModelAdminMixin

from intecomm_consent.models import SubjectConsent

from ..admin_site import intecomm_screening_admin
from ..forms import PatientLogForm
from ..models import PatientLog, SubjectScreening
from .list_filters import (
    AttendDateListFilter,
    ConsentedListFilter,
    DxListFilter,
    InPatientGroup,
    LastApptListFilter,
    NextApptListFilter,
    ScreenedListFilter,
    StableListFilter,
)
from .patient_call_inlines import AddPatientCallInline, ViewPatientCallInline


@admin.register(PatientLog, site=intecomm_screening_admin)
class PatientLogAdmin(
    SiteModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    form = PatientLogForm
    list_per_page = 20
    show_object_tools = True
    change_list_template: str = "intecomm_screening/admin/patientlog_change_list.html"

    autocomplete_fields = ["patient_group"]

    inlines = [AddPatientCallInline, ViewPatientCallInline]

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
            "Appointments",
            {
                "fields": (
                    "last_routine_appt_date",
                    "next_routine_appt_date",
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
        "hf_id",
        "dx",
        "group_name",
        "screened",
        "consented",
        "appts",
        "contacts",
        "talks",
        "site_name",
        "user_created",
        "created",
        "modified",
        "screening_identifier",
        "subject_identifier",
    )

    list_filter = (
        "report_datetime",
        "call_attempts",
        InPatientGroup,
        DxListFilter,
        StableListFilter,
        ScreenedListFilter,
        ConsentedListFilter,
        AttendDateListFilter,
        NextApptListFilter,
        LastApptListFilter,
        "first_health_talk",
        "second_health_talk",
    )

    filter_horizontal = ("conditions",)

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
        "stable": admin.VERTICAL,
        "may_contact": admin.VERTICAL,
        "first_health_talk": admin.VERTICAL,
        "second_health_talk": admin.VERTICAL,
    }

    readonly_fields = (
        "screening_identifier",
        "screening_datetime",
        "subject_identifier",
        "consent_datetime",
    )

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

    @admin.display(description="DX")
    def dx(self, obj=None):
        return [c.name.upper() for c in obj.conditions.all().order_by("name")]

    @admin.display(description="Appts", ordering="next_routine_appt_date")
    def appts(self, obj=None):
        attend_date = None
        if patient_call := obj.patientcall_set.all().order_by("report_datetime").last():
            attend_date = patient_call.attend_date or None
        context = dict(
            last_appt=obj.last_routine_appt_date or "-",
            next_appt=obj.next_routine_appt_date or "-",
            attend_date=attend_date or "-",
        )
        return format_html(
            render_to_string("intecomm_screening/change_list_appts.html", context=context)
        )

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

    @admin.display(description="Talks")
    def talks(self, obj=None):
        context = dict(
            ht1=obj.get_first_health_talk_display() or "-",
            ht2=obj.get_second_health_talk_display() or "-",
        )
        return format_html(
            render_to_string("intecomm_screening/change_list_talks.html", context=context)
        )

    @admin.display(description="Site", ordering="site")
    def site_name(self, obj=None):
        return obj.site.name.title()

    @admin.display(description="Patient", ordering="name")
    def patient(self, obj=None):
        return f"{obj.name} ({obj.initials})"

    @admin.display(description="Screen/Consent", ordering="screening_datetime")
    def screened(self, obj=None):
        add_screening_url = None
        change_screening_url = None
        add_consent_url = None
        change_consent_url = None
        if obj.screening_identifier:
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=obj.screening_identifier
            )
            change_screening_url = reverse(
                "intecomm_screening_admin:intecomm_screening_subjectscreening_change",
                args=(subject_screening.id,),
            )
        else:
            url = reverse("intecomm_screening_admin:intecomm_screening_subjectscreening_add")
            add_screening_url = (
                f"{url}?next=intecomm_screening_admin:intecomm_screening_patientlog_changelist"
                f"&hospital_identifier={obj.hf_identifier}"
                f"&initials={obj.initials}"
                f"&site={obj.site.id}"
                f"&patient_log={obj.id}"
            )
        if obj.subject_identifier:
            subject_consent = SubjectConsent.objects.get(
                screening_identifier=obj.subject_identifier
            )
            change_consent_url = reverse(
                "intecomm_consent_admin:intecomm_consent_subjectconsent_change",
                args=(subject_consent.id,),
            )
        else:
            url = reverse("intecomm_consent_admin:intecomm_consent_subjectconsent_add")
            add_consent_url = (
                f"{url}?next=intecomm_consent_admin:intecomm_consent_subjectconsent_changelist"
                f"&screening_identifier={obj.screening_identifier}"
                f"&hospital_identifier={obj.hf_identifier}"
                f"&initials={obj.initials}"
                f"&site={obj.site.id}"
            )
        context = dict(
            add_screening_url=add_screening_url,
            change_screening_url=change_screening_url,
            add_consent_url=add_consent_url,
            change_consent_url=change_consent_url,
            screening_identifier=obj.screening_identifier,
            subject_identifier=obj.subject_identifier,
        )
        return format_html(
            render_to_string(
                "intecomm_screening/change_list_screen_and_consent.html", context=context
            )
        )

    @admin.display(description="Consented", ordering="consent_datetime")
    def consented(self, obj=None):
        if obj.subject_identifier:
            return obj.consent_datetime.date()
        return None

    @admin.display(description="Group", ordering="patient_group__name")
    def group_name(self, obj=None):
        if obj.patient_group:
            url = reverse(
                "intecomm_screening_admin:intecomm_screening_patientgroup_changelist"
            )
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
