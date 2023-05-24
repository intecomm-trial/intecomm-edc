from django.contrib import admin
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import intecomm_subject_admin
from ...forms import HealthEconomicsPropertyForm
from ...models import HealthEconomicsProperty
from ..modeladmin_mixins import CrfModelAdminMixin


@admin.register(HealthEconomicsProperty, site=intecomm_subject_admin)
class HealthEconomicsPropertyAdmin(
    CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin
):
    form = HealthEconomicsPropertyForm

    additional_instructions = [
        "We want to learn about the household and we use these questions "
        "to get an understanding of wealth and opportunities in the community. "
    ]
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Property",
            {
                "description": format_html(
                    "<H5><B><font color='orange'>Interviewer to read</font></B></H5><p>"
                    "I would now like to know if you own any <B>land or other property</B> "
                    "– and the approximate value (amount). I know this is sensitive "
                    "information and will not share this with any persons outside of the "
                    "survey team. <B><U>There is no need to give details or show me any of "
                    "the items.</U></B></P>"
                ),
                "fields": (
                    "land_owner",
                    "land_value_known",
                    "land_value",
                    "land_additional",
                    "land_additional_known",
                    "land_additional_value",
                ),
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "land_owner": admin.VERTICAL,
        "land_value_known": admin.VERTICAL,
        "land_additional": admin.VERTICAL,
        "land_additional_known": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
    }
