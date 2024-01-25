from __future__ import annotations

import re
import urllib.parse
from typing import TYPE_CHECKING, Type

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from edc_consent.utils import get_remove_patient_names_from_countries
from edc_constants.choices import GENDER
from edc_constants.constants import UUID_PATTERN
from edc_sites.admin import SiteModelAdminMixin
from edc_sites.site import sites

from ...models import PatientGroup
from ..actions import render_pdf_action
from ..list_filters import (
    AttendDateListFilter,
    ConsentedListFilter,
    DxListFilter,
    InPatientGroup,
    LastApptListFilter,
    NextApptListFilter,
    ScreenedListFilter,
    StableListFilter,
)
from ..modeladmin_mixins import ChangeListTopBarModelAdminMixin
from ..patient_call_inlines import AddPatientCallInline, ViewPatientCallInline
from .change_list_template_context import ChangeListTemplateContext

if TYPE_CHECKING:
    from intecomm_consent.models import SubjectConsent, SubjectConsentUg

    from ...models import SubjectScreening, SubjectScreeningUg


class PatientLogModelAdminMixin(
    SiteModelAdminMixin,
    ChangeListTopBarModelAdminMixin,
):
    autocomplete_fields = ["site"]
    inlines = [AddPatientCallInline, ViewPatientCallInline]
    actions = [render_pdf_action]
    ordering = ("site__id", "filing_identifier")
    list_per_page = 5
    show_object_tools = True
    show_cancel = True

    list_select_related = ["site"]

    extra_pii_attrs = ["first_column"]

    change_list_note = format_html(
        "In addition to other values, you may search for patients on the last 4-digits of "
        "either their mobile number or hospital identifier."
    )
    change_list_help = (
        "Searches on encrypted data work on exact uppercase matches only. When "
        'searching on a full name, put the full name in quotations, for example, "JOHN SMITH".'
    )

    additional_instructions = format_html(
        "Only include patients that are known to have a qualifying "
        "condition and are stable in-care.<BR>"
        '<h3 style="color:orange;">Note:</h3> Log calls and call attempts at the bottom '
        "of this form."
    )

    list_display = (
        "first_column",
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
        "screening_id",
        "subject_id",
        "site",
    )

    list_filter = (
        "report_datetime",
        "willing_to_screen",
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
        "printed",
    )

    filter_horizontal = ("conditions",)

    radio_fields = {
        "first_health_talk": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "may_contact": admin.VERTICAL,
        "second_health_talk": admin.VERTICAL,
        "site": admin.VERTICAL,
        "stable": admin.VERTICAL,
        "screening_refusal_reason": admin.VERTICAL,
        "willing_to_screen": admin.VERTICAL,
    }

    readonly_fields = (
        "screening_identifier",
        "screening_datetime",
        "subject_identifier",
        "consent_datetime",
        "group_identifier",
        "filing_identifier",
        "patient_log_identifier",
        "comment",
    )

    def get_queryset(self, request) -> QuerySet:
        # TODO: does this improves performance?
        queryset = super().get_queryset(request=request)
        queryset.select_related("site").prefetch_related(
            "conditions", "patient_group", "patient_call"
        )
        return queryset

    @property
    def subject_screening_model_cls(self) -> Type[SubjectScreening, SubjectScreeningUg]:
        pass

    @property
    def subject_consent_model_cls(self) -> Type[SubjectConsent, SubjectConsentUg]:
        pass

    def post_url_on_delete_kwargs(self, request, obj):
        return {}

    @admin.display(description="Patient log", ordering="filing_identifier")
    def first_column(self, obj=None):
        legal_name = (
            "<unknown>" if re.match(UUID_PATTERN, str(obj.legal_name)) else obj.legal_name
        )
        context = dict(
            legal_name=legal_name,
            filing_identifier=obj.filing_identifier,
            last_4_hospital_identifier=obj.last_4_hospital_identifier,
            last_4_contact_number=obj.last_4_contact_number,
            initials=obj.initials,
            gender=obj.gender.upper(),
            age_in_years=obj.age_in_years,
        )
        for country in get_remove_patient_names_from_countries():
            if obj and obj.site.id in [
                s.site_id for s in sites.get_by_country(country, aslist=True)
            ]:
                context.pop("legal_name")
                break
        return format_html(
            render_to_string(
                "intecomm_screening/change_list_patient_log_first_column.html",
                context=context,
            )
        )

    @admin.display(description="Date logged", ordering="report_datetime")
    def date_logged(self, obj=None):
        return obj.report_datetime.date()

    @admin.display(description="next_appt", ordering="next_appt_date")
    def next_appt(self, obj=None):
        return obj.next_appt_date

    @admin.display(description="last_appt", ordering="last_appt_date")
    def last_appt(self, obj=None):
        return obj.last_appt_date

    @admin.display(description="FILE", ordering="filing_identifier")
    def filing_id(self, obj=None):
        context = dict(filing_identifier=obj.filing_identifier)
        return format_html(
            render_to_string(
                "intecomm_screening/change_list_filing_identifier.html", context=context
            )
        )

    @admin.display(description="Screening ID", ordering="screening_identifier")
    def screening_id(self, obj=None):
        return (
            None
            if re.match(UUID_PATTERN, obj.screening_identifier)
            else obj.screening_identifier
        )

    @admin.display(description="Subject ID", ordering="subject_identifier")
    def subject_id(self, obj=None):
        return (
            None if re.match(UUID_PATTERN, obj.subject_identifier) else obj.subject_identifier
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

    @admin.display(description="Log/Scr/Consent", ordering="screening_datetime")
    def screened(self, obj=None):
        return format_html(
            render_to_string(
                "intecomm_screening/change_list_screen_and_consent.html",
                context=self.get_screen_and_consent_template_context(obj),
            )
        )

    @admin.display(description="Log/Scr/Consent", ordering="screening_datetime")
    def screened_no_links(self, obj=None):
        return format_html(
            render_to_string(
                "intecomm_screening/change_list_screen_and_consent.html",
                context=self.get_screen_and_consent_template_context(obj),
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
            patient_group_url = reverse(
                "intecomm_screening_admin:intecomm_screening_patientgroup_changelist"
            )
            patient_group_url = (
                f"{patient_group_url}?q={urllib.parse.quote(patient_group.name)}"
            )
            context.update(
                patient_group_url=patient_group_url,
                patient_group_name=patient_group.name.replace(" ", "\n"),
                subject_identifier=obj.subject_identifier,
                subject_dashboard_url=self.get_subject_dashboard_url(obj),
            )
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
        try:
            patient_group = PatientGroup.on_site.prefetch_related("patients").get(
                name__iexact=search_term
            )
        except ObjectDoesNotExist:
            qs = qs1
        else:
            pks = [v[0] for v in queryset.values_list("id")]
            pks = [v[0] for v in patient_group.patients.filter(pk__in=pks).values_list("id")]
            qs = qs1 | self.model.on_site.filter(id__in=pks)
        return qs, True

    def get_screen_and_consent_template_context(self, obj) -> dict:
        """Context for change_list_screen_and_consent.html"""
        return ChangeListTemplateContext(
            obj,
            subject_screening_model_cls=self.subject_screening_model_cls,
            subject_consent_model_cls=self.subject_consent_model_cls,
        ).context

    @staticmethod
    def get_subject_dashboard_url(obj):
        subject_dashboard_url = None
        if obj.subject_identifier and obj.group_identifier:
            subject_dashboard_url = reverse(
                "intecomm_dashboard:subject_dashboard_url",
                args=(obj.subject_identifier,),
            )
        return subject_dashboard_url

    def report(self, obj=None):
        return format_html(
            render_to_string(
                "intecomm_screening/change_list_screen_and_consent.html",
                context=self.get_screen_and_consent_template_context(obj),
            )
        )

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "gender":
            kwargs["choices"] = GENDER
        return super().formfield_for_choice_field(db_field, request, **kwargs)
