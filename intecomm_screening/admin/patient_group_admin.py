from decimal import Decimal

import inflect
from django.apps import apps as django_apps
from django.contrib import admin
from django.db.models import Count, Q
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_constants.constants import COMPLETE, DM, HIV, HTN, NEW
from edc_utils.round_up import round_up
from intecomm_form_validators import RECRUITING
from intecomm_form_validators.utils import get_min_group_size_for_ratio

from intecomm_group.exceptions import PatientGroupNotRandomized
from intecomm_group.utils import (
    get_assignment_description_for_patient_group,
    verify_patient_group_ratio_raise,
)

from ..admin_site import intecomm_screening_admin
from ..forms import PatientGroupForm
from ..models import PatientGroup
from .modeladmin_mixins import BaseModelAdminMixin

p = inflect.engine()


@admin.register(PatientGroup, site=intecomm_screening_admin)
class PatientGroupAdmin(BaseModelAdminMixin):

    form = PatientGroupForm

    show_object_tools = True
    change_list_template: str = "intecomm_screening/admin/patientgroup_change_list.html"
    change_list_help = "Searches on encrypted data work on exact uppercase matches only"
    change_list_title = PatientGroup._meta.verbose_name_plural

    fieldsets = (
        (
            None,
            {"fields": ("report_datetime", "name")},
        ),
        (
            "Patients",
            {
                "fields": (
                    "hiv_patients",
                    "dm_patients",
                    "htn_patients",
                    "multi_patients",
                ),
            },
        ),
        (
            "Selected Patients",
            {
                "description": (
                    "Changes made above will be reflected here after the form is saved."
                ),
                "fields": ("patients",),
            },
        ),
        (
            "Notes",
            {"fields": ("notes",)},
        ),
        (
            "Status, Size, Ratio",
            {
                "description": format_html(
                    "Please consult with your study coordinator before you "
                    "choose to override the minimum group size and/or the ratio of "
                    "NCD to HIV patients."
                ),
                "fields": (
                    "status",
                    "bypass_group_size_min",
                    "bypass_group_ratio",
                ),
            },
        ),
        (
            "Randomize",
            {
                "description": format_html(
                    "Complete this section when the group is COMPLETE and ready to "
                    "RANDOMIZE. <BR>Please consult with your study coordinator before "
                    "randomizing a group that does not meet the minimum group size and/or "
                    "the ratio of NCD to HIV patients. <BR>"
                    "<B>Important: THIS STEP CANNOT BE UNDONE</B>"
                ),
                "fields": (
                    "randomize_now",
                    "confirm_randomize_now",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "__str__",
        "opened",
        "status",
        "rounded_ratio",
        "arm",
        "members",
        "user_created",
        "created",
    )

    list_filter = (
        "status",
        "randomized",
        "report_datetime",
    )

    search_fields = (
        "name",
        "hiv_patients__legal_name__exact",
        "hiv_patients__familiar_name__exact",
        "hiv_patients__initials__iexact",
        "dm_patients__legal_name__exact",
        "dm_patients__familiar_name__exact",
        "dm_patients__initials__iexact",
        "htn_patients__legal_name__exact",
        "htn_patients__familiar_name__exact",
        "htn_patients__initials__iexact",
    )

    filter_horizontal = (
        "hiv_patients",
        "dm_patients",
        "htn_patients",
        "multi_patients",
        "patients",
    )

    radio_fields = {
        "status": admin.VERTICAL,
        "randomize_now": admin.VERTICAL,
    }

    readonly_fields = ("patients",)

    @admin.display(description="Opened", ordering="report_datetime")
    def opened(self, obj=None):
        return obj.report_datetime.date()

    @admin.display(description="Patients")
    def members(self, obj=None):
        cnt = (
            obj.hiv_patients.all().count()
            + obj.dm_patients.all().count()
            + obj.htn_patients.all().count()
            + obj.multi_patients.all().count()
        )
        cnt1 = obj.patients.all().count()
        url = reverse("intecomm_screening_admin:intecomm_screening_patientlog_changelist")
        url = f"{url}?q={obj.name}"
        return format_html(
            f'<a href="{url}">{cnt}&nbsp;{p.plural("patient", cnt)}({cnt1})</a>'
        )

    @admin.display(description="Arm")
    def arm(self, obj=None):
        try:
            return get_assignment_description_for_patient_group(obj.group_identifier)
        except PatientGroupNotRandomized:
            return None

    @admin.display(description="NCD:HIV", ordering="ratio")
    def rounded_ratio(self, obj=None):
        patients = obj.hiv_patients.all() | obj.dm_patients.all() | obj.htn_patients.all()
        ncd, hiv, ratio = verify_patient_group_ratio_raise(patients)
        ratio_str = ""
        if patients.count() >= get_min_group_size_for_ratio():
            ratio = round_up(ratio or Decimal("0.00"), Decimal("2.00"))
            ratio_str = f" ({str(ratio)})"
        return f"{ncd}:{hiv}{ratio_str}"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(status__in=[NEW, RECRUITING, COMPLETE], randomized=False)
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            patient_log_model_cls = django_apps.get_model("intecomm_screening.patientlog")
            conditions = [HIV, DM, HTN]
            for cond in conditions:
                q_lookup = Q(patientgroup__isnull=True)
                if obj:
                    q_lookup = q_lookup | Q(patientgroup__name=obj.name)
                q_lookup = q_lookup, Q(conditions__name=cond)
                form.base_fields[
                    f"{cond.lower()}_patients"
                ].queryset = patient_log_model_cls.objects.filter(*q_lookup).exclude(
                    Q(conditions__name__in=[c for c in conditions if c != cond])
                )

            # multimorbidity
            qs = (
                patient_log_model_cls.objects.filter(
                    Q(patientgroup__name=obj.name) | Q(patientgroup__isnull=True)
                )
                .values("id")
                .annotate(conditions_count=Count("conditions__name"))
            )
            multi_morbidity_pks = [o.get("id") for o in qs if o.get("conditions_count") > 1]
            form.base_fields["multi_patients"].queryset = patient_log_model_cls.objects.filter(
                pk__in=multi_morbidity_pks
            )

        return form
