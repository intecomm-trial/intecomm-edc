import re
from decimal import Decimal
from typing import Tuple

import inflect
from django.apps import apps as django_apps
from django.contrib import admin
from django.db.models import Count, Q
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_constants.constants import COMPLETE, DM, HIV, HTN, UUID_PATTERN, YES
from edc_utils.round_up import round_up
from intecomm_form_validators.utils import get_group_size_for_ratio

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
            "Size, Ratio",
            {
                "description": format_html(
                    "Please consult with your study coordinator before you "
                    "choose to override the minimum group size and/or the ratio of "
                    "NCD to HIV patients."
                ),
                "fields": (
                    "bypass_group_size_min",
                    "bypass_group_ratio",
                ),
            },
        ),
        (
            "Status",
            {
                "description": format_html(
                    "<P>Patients may be selected if <B>status</B> is "
                    "set to <U>Recruiting</U>. Once patient selections are final, "
                    "set <B>status</B> to <U>Complete</U>."
                    "<BR>If you need to make changes after setting <B>status</B> "
                    "to <U>Complete</U>:"
                    "<BR>-set the <B>status</B> back to <U>Recruiting</U>;"
                    "<BR>-save this form;"
                    "<BR>-reopen this form and make your changes.</P>"
                ),
                "fields": ("status",),
            },
        ),
        (
            "Randomization",
            {
                "fields": ("group_identifier", "randomized", "randomized_datetime"),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "__str__",
        "opened",
        "group_status",
        "rounded_ratio",
        "arm",
        "to_patients",
        "group_id",
        "randomized_date",
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
        "group_identifier",
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

    radio_fields = {"status": admin.VERTICAL}

    readonly_fields = ("patients", "group_identifier", "randomized", "randomized_datetime")

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.randomized:
            fieldsets = [
                fieldset
                for fieldset in fieldsets
                if fieldset[0] not in ["Selected Patients", "Randomize"]
            ]
        else:
            fieldsets = [
                fieldset for fieldset in fieldsets if fieldset[0] not in ["Randomization"]
            ]
        fieldsets = tuple(fieldsets)
        return fieldsets

    def get_readonly_fields(self, request, obj=None) -> Tuple[str, ...]:
        fields = super().get_readonly_fields(request, obj)
        if obj and obj.randomized:
            fields += (
                "report_datetime",
                "hiv_patients",
                "dm_patients",
                "htn_patients",
                "multi_patients",
                "bypass_group_size_min",
                "bypass_group_ratio",
                "status",
            )
        return fields

    @admin.display(description="Opened", ordering="report_datetime")
    def opened(self, obj=None):
        return obj.report_datetime.date()

    @admin.display(description="Randomized", ordering="randomized_datetime")
    def randomized_date(self, obj=None):
        try:
            return obj.randomized_datetime.date()
        except AttributeError:
            return None

    @admin.display(description="Group identifier", ordering="group_identifier")
    def group_id(self, obj):
        return (
            None if re.match(UUID_PATTERN, str(obj.group_identifier)) else obj.group_identifier
        )

    @admin.display(description="Status", ordering="status")
    def group_status(self, obj):
        return format_html(f'<span class="nowrap">{obj.get_status_display()}</span>')

    @admin.display(description="Patient Logs")
    def to_patients(self, obj=None):
        cnt = obj.patients.all().count()
        url = reverse("intecomm_screening_admin:intecomm_screening_patientlog_changelist")
        url = f"{url}?q={obj.name}"
        return format_html(
            f'<a title="Go to patient log" href="{url}">'
            f'<span class="nowrap">{cnt}&nbsp;{p.plural("patient", cnt)}</span></a>'
        )

    @admin.display(description="Randomization")
    def arm(self, obj=None):
        try:
            arm_as_str = get_assignment_description_for_patient_group(obj.group_identifier)
        except PatientGroupNotRandomized:
            if obj.status == COMPLETE:
                url = reverse(
                    "intecomm_screening_admin:intecomm_screening_patientgrouprando_change",
                    args=(obj.id,),
                )
                url = f"{url}?name={obj.name}"
                link = format_html(
                    f'<a title="Go to Patient group rando" href="{url}">Ready to randomize</a>'
                )
            else:
                link = None
        else:
            url = reverse("intecomm_group_admin:intecomm_group_patientgroup_changelist")
            url = f"{url}?q={obj.name}"
            link = format_html(
                f'<a title="Go to patient groups in followup" href="{url}">{arm_as_str}</a>'
            )
        return link

    @admin.display(description="NCD:HIV", ordering="ratio")
    def rounded_ratio(self, obj=None):
        patients = obj.hiv_patients.all() | obj.dm_patients.all() | obj.htn_patients.all()
        ncd, hiv, ratio = verify_patient_group_ratio_raise(patients)
        ratio_str = ""
        if patients.count() >= get_group_size_for_ratio():
            ratio = round_up(ratio or Decimal("0.00"), Decimal("2.00"))
            ratio_str = f" ({str(ratio)})"
        return f"{ncd}:{hiv}{ratio_str}"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if (
            obj
            and not obj.randomized
            and request.user.has_perm("intecomm_screening.change_patientlog")
        ):
            patient_log_model_cls = django_apps.get_model("intecomm_screening.patientlog")
            conditions = [HIV, DM, HTN]
            q_lookup = Q(patientgroup__isnull=True) | Q(patientgroup__name=obj.name)
            for cond in conditions:
                form.base_fields[
                    f"{cond.lower()}_patients"
                ].queryset = patient_log_model_cls.objects.filter(
                    q_lookup, stable=YES, site_id=obj.site_id, conditions__name=cond
                ).exclude(
                    Q(conditions__name__in=[c for c in conditions if c != cond])
                )

            # multimorbidity
            qs = (
                patient_log_model_cls.objects.filter(q_lookup, stable=YES, site_id=obj.site_id)
                .values("id")
                .annotate(conditions_count=Count("conditions__name"))
            )
            multi_morbidity_pks = [o.get("id") for o in qs if o.get("conditions_count") > 1]
            form.base_fields["multi_patients"].queryset = patient_log_model_cls.objects.filter(
                pk__in=multi_morbidity_pks
            )
        return form
