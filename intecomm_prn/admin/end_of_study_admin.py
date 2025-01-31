from __future__ import annotations

from dateutil.relativedelta import relativedelta
from django.contrib import admin
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item import ActionItemModelAdminMixin, action_fieldset_tuple
from edc_constants.constants import OTHER
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from intecomm_ae.models import DeathReport
from intecomm_consent.models import SubjectConsent

from ..admin_site import intecomm_prn_admin
from ..forms import EndOfStudyForm
from ..models import EndOfStudy, LossToFollowup


@admin.register(EndOfStudy, site=intecomm_prn_admin)
class EndOfStudyAdmin(
    SiteModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    ActionItemModelAdminMixin,
    SimpleHistoryAdmin,
):
    additional_instructions = format_html(
        "{}",
        "Note: if the patient is <i>deceased</i>, complete form "
        "`{}` before completing this form. "
        "<BR>If the patient is </i>lost to follow up</i>, complete form "
        "`{}` before completing this form.",
        DeathReport._meta.verbose_name,
        LossToFollowup._meta.verbose_name,
    )

    form = EndOfStudyForm

    date_hierarchy = "offstudy_datetime"

    fieldsets = (
        [
            None,
            {
                "fields": (
                    "subject_identifier",
                    "offstudy_datetime",
                    "last_seen_date",
                )
            },
        ],
        [
            "Off-study reason",
            {
                "fields": (
                    "offstudy_reason",
                    "other_offstudy_reason",
                )
            },
        ],
        [
            "Dates from supporting documents (if applicable)",
            {
                "fields": (
                    "ltfu_date",
                    "transfer_date",
                    "death_date",
                )
            },
        ],
        [
            "Withdrawn on CLINICAL grounds (if applicable)",
            {
                "description": (
                    "This section is applicable if the patient was withdrawn "
                    "on clinical grounds, as indicated above"
                ),
                "fields": (
                    "clinical_withdrawal_reason",
                    "clinical_withdrawal_investigator_decision",
                    "clinical_withdrawal_reason_other",
                ),
            },
        ],
        [
            "Comment",
            {"fields": ("comment",)},
        ],
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "offstudy_reason": admin.VERTICAL,
        "clinical_withdrawal_reason": admin.VERTICAL,
    }

    def get_list_display(self, request) -> tuple[str, ...]:
        list_display = super().get_list_display(request)
        custom_fields = (
            "subject_identifier",
            "dashboard",
            "terminated",
            "last_seen",
            "months",
            "reason",
        )
        return custom_fields + tuple(
            f for f in list_display if f not in custom_fields + ("__str__",)
        )

    # TODO: remove `self.list_filter = list_filter` with Django > 4.2.5
    def get_list_filter(self, request) -> tuple[str, ...]:
        list_filter = super().get_list_filter(request)
        custom_fields = ("offstudy_reason", "last_seen_date")
        list_filter = custom_fields + tuple(f for f in list_filter if f not in custom_fields)
        self.list_filter = list_filter
        return list_filter

    def get_search_fields(self, request) -> tuple[str, ...]:
        search_fields = super().get_search_fields(request)
        custom_fields = ("subject_identifier",)
        return tuple(set(custom_fields + search_fields))

    @admin.display(description="terminated", ordering="offstudy_datetime")
    def terminated(self, obj):
        return obj.offstudy_datetime.date()

    @admin.display(description="last_seen", ordering="last_seen_date")
    def last_seen(self, obj):
        return obj.last_seen_date

    @admin.display(description="Offstudy reason", ordering="offstudy_reason")
    def reason(self, obj):
        return (
            obj.offstudy_reason if obj.offstudy_reason != OTHER else obj.other_offstudy_reason
        )

    @admin.display(description="M")
    def months(self, obj):
        subject_consent = SubjectConsent.objects.get(subject_identifier=obj.subject_identifier)
        return relativedelta(obj.offstudy_datetime, subject_consent.consent_datetime).months
