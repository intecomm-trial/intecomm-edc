from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields import audit_fieldset_tuple
from edc_constants.choices import GENDER

from ..admin_site import intecomm_screening_admin
from ..forms import PatientLogForm
from ..models import PatientGroup, PatientLog, SubjectScreening
from ..utils import get_add_or_change_consent_url
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
from .modeladmin_mixins import BaseModelAdminMixin
from .patient_call_inlines import AddPatientCallInline, ViewPatientCallInline


@admin.register(PatientLog, site=intecomm_screening_admin)
class PatientLogAdmin(BaseModelAdminMixin):

    form = PatientLogForm
    list_per_page = 20
    show_object_tools = True
    show_cancel = True
    change_list_template: str = "intecomm_screening/admin/patientlog_change_list.html"
    change_list_title = PatientLog._meta.verbose_name
    change_list_note = format_html(
        "In addition to other values, you may search for patients on the last 4-digits of "
        "either their mobile number or hospital identifier."
    )
    change_list_help = (
        "Searches on encrypted data work on exact uppercase matches only. When "
        'searching on a full name, put the full name in quotations, for example, "JOHN SMITH".'
    )

    autocomplete_fields = ["site"]

    inlines = [AddPatientCallInline, ViewPatientCallInline]

    additional_instructions = format_html(
        "Only include patients that are known to have a qualifying "
        "condition and are stable in-care.<BR>"
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
            "Name and basic demographics",
            {
                "fields": (
                    "legal_name",
                    "familiar_name",
                    "initials",
                    "hospital_identifier",
                    "gender",
                    "age_in_years",
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
            {"fields": ("location_description",)},
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
                    "last_appt_date",
                    "next_appt_date",
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
        "__str__",
        "hf_id",
        "dx",
        "group_name",
        "screened",
        "appts",
        "contacts",
        "talks",
        "site_id",
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
        "gender",
    )

    filter_horizontal = ("conditions",)

    search_fields = (
        "id",
        "screening_identifier",
        "subject_identifier",
        "last_4_hospital_identifier__exact",
        "last_4_contact_number__exact",
        "hospital_identifier__exact",
        "initials__exact",
        "legal_name__exact",
        "familiar_name__exact",
        "contact_number__exact",
        "alt_contact_number__exact",
    )

    radio_fields = {
        "first_health_talk": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "may_contact": admin.VERTICAL,
        "second_health_talk": admin.VERTICAL,
        "stable": admin.VERTICAL,
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

    @admin.display(description="next_appt", ordering="next_appt_date")
    def next_appt(self, obj=None):
        return obj.next_appt_date

    @admin.display(description="last_appt", ordering="last_appt_date")
    def last_appt(self, obj=None):
        return obj.last_appt_date

    @admin.display(description="HF ID", ordering="hospital_identifier")
    def hf_id(self, obj=None):
        context = dict(hospital_identifier=obj.hospital_identifier)
        return format_html(
            render_to_string(
                "intecomm_screening/change_list_hospital_identifier.html", context=context
            )
        )

    @admin.display(description="DX")
    def dx(self, obj=None):
        context = dict(
            diagnoses=[c.name.upper() for c in obj.conditions.all().order_by("name")]
        )
        return format_html(
            render_to_string("intecomm_screening/change_list_dx.html", context=context)
        )

    @admin.display(description="Appts", ordering="next_appt_date")
    def appts(self, obj=None):
        context = dict(
            last_appt=obj.last_appt_date or "-",
            next_appt=obj.next_appt_date or "-",
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
            ht1=obj.first_health_talk,
            ht2=obj.second_health_talk,
        )
        return format_html(
            render_to_string("intecomm_screening/change_list_talks.html", context=context)
        )

    @admin.display(description="Site", ordering="site")
    def site_id(self, obj=None):
        return obj.site.id

    @admin.display(description="Patient", ordering="familiar_name")
    def patient(self, obj=None):
        return f"{obj.familiar_name} ({obj.initials})"

    @admin.display(description="Screen/Consent", ordering="screening_datetime")
    def screened(self, obj=None):
        return format_html(
            render_to_string(
                "intecomm_screening/change_list_screen_and_consent.html",
                context=self.get_screening_context(obj),
            )
        )

    @admin.display(description="Consented", ordering="consent_datetime")
    def consented(self, obj=None):
        if obj.subject_identifier:
            return obj.consent_datetime.date()
        return None

    @admin.display(description="Group", ordering="patientgroup__name")
    def group_name(self, obj=None):
        context = dict()
        if obj.patientgroup_set.all().count() > 0:
            patient_group = obj.patientgroup_set.all().first()
            url = reverse(
                "intecomm_screening_admin:intecomm_screening_patientgroup_changelist"
            )
            url = f"{url}?q={patient_group.name}"
            context.update(url=url, patient_group=patient_group)
        return format_html(
            render_to_string("intecomm_screening/change_list_group.html", context=context)
        )

    @admin.display(description="Calls", ordering="contact_attempts")
    def calls(self, obj):
        url = reverse("intecomm_screening_admin:intecomm_screening_patientcall_changelist")
        url = f"{url}?q={obj.patientcall.id}"
        return format_html(f'<A href="{url}">{obj.contact_attempts}</a>')

    def get_search_results(self, request, queryset, search_term):
        """Union initial search queryset (qs1) with
        patients in a group whose name matches the search term (qs2).

        Note: queryset is a queryset already passed through the
        changelist's filters.
        """
        qs1, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        queryset_pks = [obj.pk for obj in queryset.all()]
        try:
            patient_group = PatientGroup.objects.get(name__iexact=search_term)
        except ObjectDoesNotExist:
            qs = qs1
        else:
            pks = [obj.pk for obj in patient_group.patients.filter(pk__in=queryset_pks)]
            qs = qs1 | self.model.objects.filter(id__in=pks)
        return qs, True

    @staticmethod
    def get_screening_context(obj) -> dict:
        add_screening_url = None
        change_screening_url = None
        add_consent_url = None
        change_consent_url = None
        subject_identifier = None
        subject_screening = None
        eligible = None
        if obj.screening_identifier:
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=obj.screening_identifier
            )
            eligible = subject_screening.eligible
            url = reverse(
                "intecomm_screening_admin:intecomm_screening_subjectscreening_change",
                args=(subject_screening.id,),
            )
            change_screening_url = (
                f"{url}?next=intecomm_screening_admin:intecomm_screening_patientlog_changelist"
                f"&q={obj.screening_identifier}"
            )
        else:
            url = reverse("intecomm_screening_admin:intecomm_screening_subjectscreening_add")
            add_screening_url = (
                f"{url}?next=intecomm_screening_admin:intecomm_screening_patientlog_changelist"
                f"&hospital_identifier={obj.hospital_identifier}"
                f"&initials={obj.initials}"
                f"&site={obj.site.id}"
                f"&gender={obj.gender}"
                f"&age_in_years={obj.age_in_years}"
                f"&legal_name={obj.legal_name}"
                f"&familiar_name={obj.familiar_name}"
                f"&patient_log={obj.id}"
                f"&q={obj.screening_identifier}"
            )
        if subject_screening and subject_screening.eligible:
            (
                add_consent_url,
                change_consent_url,
                subject_identifier,
            ) = get_add_or_change_consent_url(subject_screening)

        return dict(
            add_screening_url=add_screening_url,
            change_screening_url=change_screening_url,
            add_consent_url=add_consent_url,
            change_consent_url=change_consent_url,
            screening_identifier=obj.screening_identifier,
            subject_identifier=subject_identifier,
            eligible=eligible,
        )

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "gender":
            kwargs["choices"] = GENDER
        return super().formfield_for_choice_field(db_field, request, **kwargs)
