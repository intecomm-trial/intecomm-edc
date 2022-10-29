from django import forms
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import BLANK_CHOICE_DASH
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.modeladmin_mixins import SiteModelAdminMixin

from ..admin_site import intecomm_screening_admin
from ..constants import RECRUITING
from ..forms import PatientLogForm
from ..models import PatientGroup, PatientLog


class ActionForm(forms.Form):
    action = forms.ChoiceField(label="Action:")
    group = forms.ChoiceField(
        label="Group:",
        required=True,
        choices=(
            ((None, BLANK_CHOICE_DASH),)
            + tuple(
                (o.id, o.name)
                for o in PatientGroup.objects.filter(status=RECRUITING).order_by("name")
            )
        ),
    )
    select_across = forms.BooleanField(
        label="",
        required=False,
        initial=0,
        widget=forms.HiddenInput({"class": "select-across"}),
    )


@admin.register(PatientLog, site=intecomm_screening_admin)
class PatientLogAdmin(
    SiteModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    form = PatientLogForm
    action_form = ActionForm
    list_per_page = 20
    show_object_tools = True

    # post_url_on_delete_name = "screening_listboard_url"
    # subject_listboard_url_name = "screening_listboard_url"

    additional_instructions = (
        "Only include patients that are known to have a qualifying "
        "condition and are stable in-care."
    )

    actions = ["to_group"]

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
                    "contact_number",
                    "alt_contact_number",
                )
            },
        ),
        (
            "Location",
            {"fields": ("location_description",)},
        ),
        (
            "Health",
            {
                "fields": (
                    "conditions",
                    "stable",
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
        "hf_id",
        "patient",
        "group_name",
        "date_logged",
        "contact_number",
        "alternate",
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
        "first_health_talk",
        "second_health_talk",
        "report_datetime",
        "site",
    )

    filter_horizontal = ("conditions",)

    search_fields = (
        "screening_identifier",
        "subject_identifier",
        "hf_identifier",
        "initials",
        "name",
    )

    radio_fields = {
        "stable": admin.VERTICAL,
        "first_health_talk": admin.VERTICAL,
        "second_health_talk": admin.VERTICAL,
    }

    readonly_fields = ("screening_identifier", "screening_datetime", "subject_identifier")

    def post_url_on_delete_kwargs(self, request, obj):
        return {}

    @admin.display(description="Date logged", ordering="report_datetime")
    def date_logged(self, obj=None):
        return obj.report_datetime.date()

    @admin.display(description="HF ID", ordering="hf_identifier")
    def hf_id(self, obj=None):
        return obj.hf_identifier

    @admin.display(description="Alternate", ordering="alt_contact_number")
    def alternate(self, obj=None):
        return obj.alt_contact_number

    @admin.display(description="1st HT", ordering="first_health_talk")
    def ht1(self, obj=None):
        return obj.first_health_talk

    @admin.display(description="2nd HT", ordering="second_health_talk")
    def ht2(self, obj=None):
        return obj.second_health_talk

    @admin.display(description="Site", ordering="site")
    def site_name(self, obj=None):
        return obj.site.name.title()

    @admin.display(description="Patient", ordering="name")
    def patient(self, obj=None):
        return f"{obj.name} ({obj.initials})"

    @admin.display(description="Group")
    def group_name(self, obj=None):
        try:
            patient_group = PatientGroup.objects.get(patients__pk=obj.id)
        except ObjectDoesNotExist:
            pass
        else:
            group_name = patient_group.name
            if patient_group:
                url = reverse(
                    "intecomm_screening_admin:intecomm_screening_patientgroup_changelist"
                )
                url = f"{url}?q={group_name}"
                return format_html(f'<a href="{url}">{group_name}</a>')
        return None

    @admin.action(description="Add patients to ")
    def to_group(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        group_pk = request.POST["group"]
        if group_pk:
            try:
                patient_group = PatientGroup.objects.get(id=group_pk)
            except ObjectDoesNotExist:
                patient_group = PatientGroup.objects.create()
            for pk in selected:
                patient_log = queryset.model.objects.get(id=pk)
                if not patient_group.patients.filter(id=pk).exists():
                    patient_group.patients.add(patient_log)
            url = reverse(
                "intecomm_screening_admin:intecomm_screening_patientgroup_change",
                args=(patient_group.id,),
            )
            return HttpResponseRedirect(url)
        return None
        # return self.message_user(request, "No group selected", level=messages.WARNING)

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
