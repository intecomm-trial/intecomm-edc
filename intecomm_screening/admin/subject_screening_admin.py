from typing import Tuple

from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django_audit_fields import audit_fieldset_tuple
from edc_constants.choices import GENDER
from edc_dashboard.url_names import url_names
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_screening.utils import format_reasons_ineligible
from edc_sites.modeladmin_mixins import SiteModelAdminMixin

from ..admin_site import intecomm_screening_admin
from ..forms import SubjectScreeningForm
from ..models import PatientLog, SubjectScreening


@admin.register(SubjectScreening, site=intecomm_screening_admin)
class SubjectScreeningAdmin(
    SiteModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    form = SubjectScreeningForm
    list_per_page = 15
    post_url_on_delete_name = "screening_listboard_url"
    subject_listboard_url_name = "screening_listboard_url"

    subject_dashboard_url_name = "screening_listboard_url"

    change_list_template: str = "intecomm_screening/admin/subjectscreening_change_list.html"

    additional_instructions = (
        "Patients must meet ALL of the inclusion criteria and NONE of the "
        "exclusion criteria in order to proceed to the final screening stage"
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "report_datetime",
                    "site",
                    "patient_log",
                )
            },
        ),
        (
            "Demographics",
            {
                "description": (
                    "Please review carefully. If anything needs to be changed, do so on "
                    "the Patient Log and try again"
                ),
                "fields": (
                    "legal_name",
                    "familiar_name",
                    "initials",
                    "hospital_identifier",
                    "gender",
                    "age_in_years",
                ),
            },
        ),
        (
            "Health facility",
            {
                "fields": (
                    "in_care_6m",
                    "in_care_duration",
                )
            },
        ),
        (
            "HIV",
            {
                "fields": (
                    "hiv_dx",
                    "hiv_dx_6m",
                    "hiv_dx_ago",
                    "art_unchanged_3m",
                    "art_stable",
                    "art_adherent",
                )
            },
        ),
        (
            "Diabetes",
            {
                "fields": (
                    "dm_dx",
                    "dm_dx_6m",
                    "dm_dx_ago",
                    "dm_complications",
                )
            },
        ),
        (
            "Hypertension",
            {
                "fields": (
                    "htn_dx",
                    "htn_dx_6m",
                    "htn_dx_ago",
                    "htn_complications",
                )
            },
        ),
        (
            "Pregnancy",
            {"fields": ("pregnant",)},
        ),
        (
            "Other history",
            {
                "fields": (
                    "excluded_by_bp_history",
                    "excluded_by_gluc_history",
                    "requires_acute_care",
                )
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "lives_nearby",
                    "staying_nearby_6",
                )
            },
        ),
        (
            "Blood pressure measurements",
            {
                "fields": (
                    "sys_blood_pressure_one",
                    "dia_blood_pressure_one",
                    "sys_blood_pressure_two",
                    "dia_blood_pressure_two",
                )
            },
        ),
        (
            "Other",
            {
                "fields": (
                    "consent_ability",
                    "unsuitable_for_study",
                    "reasons_unsuitable",
                    "unsuitable_agreed",
                )
            },
        ),
        (
            "Updates",
            {
                "classes": ("collapse",),
                "fields": (
                    "screening_identifier",
                    "eligible",
                    "eligibility_datetime",
                    "real_eligibility_datetime",
                    "subject_identifier",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "screening_identifier",
        "eligibility_status",
        "demographics",
        "reasons",
        "report_datetime",
        "user_created",
        "created",
    )

    list_filter = (
        "report_datetime",
        "gender",
        "eligible",
        "consented",
        "refused",
    )

    search_fields = (
        "screening_identifier",
        "subject_identifier",
        "hospital_identifier",
        "initials",
        "reasons_ineligible",
    )

    readonly_fields = (
        "screening_identifier",
        "eligible",
        "eligibility_datetime",
        "real_eligibility_datetime",
        "subject_identifier",
    )

    radio_fields = {
        "consent_ability": admin.VERTICAL,
        "dm_dx": admin.VERTICAL,
        "dm_dx_6m": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "hiv_dx": admin.VERTICAL,
        "hiv_dx_6m": admin.VERTICAL,
        "htn_dx": admin.VERTICAL,
        "htn_dx_6m": admin.VERTICAL,
        "selection_method": admin.VERTICAL,
        "lives_nearby": admin.VERTICAL,
        "staying_nearby_6": admin.VERTICAL,
        "in_care_6m": admin.VERTICAL,
        "art_unchanged_3m": admin.VERTICAL,
        "art_stable": admin.VERTICAL,
        "art_adherent": admin.VERTICAL,
        "dm_complications": admin.VERTICAL,
        "htn_complications": admin.VERTICAL,
        "pregnant": admin.VERTICAL,
        "excluded_by_bp_history": admin.VERTICAL,
        "excluded_by_gluc_history": admin.VERTICAL,
        "requires_acute_care": admin.VERTICAL,
        "unsuitable_for_study": admin.VERTICAL,
        "unsuitable_agreed": admin.VERTICAL,
    }

    def post_url_on_delete_kwargs(self, request, obj):
        return {}

    def get_readonly_fields(self, request, obj=None) -> Tuple[str, ...]:
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj:
            readonly_fields = readonly_fields + ("patient_log",)
        return readonly_fields

    @staticmethod
    def demographics(obj=None):
        data = [
            f"{obj.get_gender_display()} {obj.age_in_years}yrs",
            f"Initials: {obj.initials.upper()}<BR>",
            f"Hospital ID: {obj.hospital_identifier}",
        ]
        return format_html("<BR>".join(data))

    def reasons(self, obj=None):
        if not obj.reasons_ineligible:
            return self.dashboard(obj)
        return format_reasons_ineligible(obj.reasons_ineligible)

    def eligibility_status(self, obj=None):
        return None
        # eligibility = ScreeningEligibility(update_model=False)
        # screening_listboard_url = reverse(
        #     url_names.get(self.subject_listboard_url_name), args=(obj.screening_identifier,)
        # )
        # context = dict(
        #     title=_("Go to screening listboard"),
        #     url=f"{screening_listboard_url}?q={obj.screening_identifier}",
        #     label="Screening",
        # )
        # button = render_to_string("dashboard_button.html", context=context)
        # return format_html(button + "<BR>" + eligibility.eligibility_status(add_urls=True))

    def dashboard(self, obj=None, label=None):
        try:
            url = reverse(
                self.get_subject_dashboard_url_name(),
                kwargs=self.get_subject_dashboard_url_kwargs(obj),
            )
        except NoReverseMatch:
            url = reverse(url_names.get("screening_listboard_url"), kwargs={})
            context = dict(
                title=_("Go to screening and consent"),
                url=f"{url}?q={obj.screening_identifier}",
                label=label,
            )
        else:
            context = dict(title=_("Go to subject dashboard"), url=url, label=label)
        return render_to_string("dashboard_button.html", context=context)

    def formfield_for_foreignkey(self, db_field, request: WSGIRequest, **kwargs):
        db = kwargs.get("using")
        if db_field.name == "patient_log":
            if request.GET.get("patient_log"):
                kwargs["queryset"] = PatientLog.objects.using(db).filter(
                    id__exact=request.GET.get("patient_log", 0)
                )
            else:
                kwargs["queryset"] = PatientLog.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def view_on_site(self, obj) -> str:
        return reverse(self.get_subject_listboard_url_name())

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "gender":
            kwargs["choices"] = GENDER
        return super().formfield_for_choice_field(db_field, request, **kwargs)
