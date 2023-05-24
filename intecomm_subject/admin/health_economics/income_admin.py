from django.contrib import admin
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import intecomm_subject_admin
from ...forms import HealthEconomicsIncomeForm
from ...models import HealthEconomicsIncome
from ..modeladmin_mixins import CrfModelAdminMixin


@admin.register(HealthEconomicsIncome, site=intecomm_subject_admin)
class HealthEconomicsIncomeAdmin(
    CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin
):
    form = HealthEconomicsIncomeForm

    additional_instructions = [
        "We want to learn about the household and we use these questions "
        "to get an understanding of wealth and opportunities in the community. "
    ]
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Household income",
            {
                "description": format_html(
                    "Now, I will ask about income for the household from paid work or "
                    "other sources. I know it may be difficult to calculate those figures, "
                    "but please do try to give amounts as accurately as possible. Remember "
                    "that all information will be kept strictly confidential. This "
                    "information is important to assess overall health and well-being of "
                    "people in your household, compared to other similar households.<BR><BR>"
                    "I am now going to read you a list of possible sources of income. "
                    "Thinking over the last 12 months, can you tell me what the average "
                    "earnings of the household have been per week or per month or per year? "
                    "Please tell me whichever time period that is easier for you."
                ),
                "fields": (
                    "wages",
                    "wages_value_known",
                    "wages_value",
                    "selling",
                    "selling_value_known",
                    "selling_value",
                    "rental_income",
                    "rental_income_value_known",
                    "rental_income_value",
                    "pension",
                    "pension_value_known",
                    "pension_value",
                    "ngo_assistance",
                    "ngo_assistance_value_known",
                    "ngo_assistance_value",
                    "interest",
                    "interest_value_known",
                    "interest_value",
                    "internal_remittance",
                    "internal_remittance_value_known",
                    "internal_remittance_value",
                    "external_remittance",
                    "external_remittance_value_known",
                    "external_remittance_value",
                    "external_remittance_currency",
                    "external_remittance_currency_other",
                    "more_sources",
                    "more_sources_other",
                    "more_sources_value_known",
                    "more_sources_value",
                    "external_dependents",
                    "income_enough",
                    "financial_status",
                    "financial_status_compare",
                    "household_debt",
                    "household_debt_value",
                ),
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "wages": admin.VERTICAL,
        "wages_value_known": admin.VERTICAL,
        "selling": admin.VERTICAL,
        "selling_value_known": admin.VERTICAL,
        "rental_income": admin.VERTICAL,
        "rental_income_value_known": admin.VERTICAL,
        "pension": admin.VERTICAL,
        "pension_value_known": admin.VERTICAL,
        "ngo_assistance": admin.VERTICAL,
        "ngo_assistance_value_known": admin.VERTICAL,
        "interest": admin.VERTICAL,
        "interest_value_known": admin.VERTICAL,
        "internal_remittance": admin.VERTICAL,
        "internal_remittance_value_known": admin.VERTICAL,
        "external_remittance": admin.VERTICAL,
        "external_remittance_value_known": admin.VERTICAL,
        "external_remittance_currency": admin.VERTICAL,
        "more_sources": admin.VERTICAL,
        "more_sources_value_known": admin.VERTICAL,
        # "external_dependents": admin.VERTICAL,
        "income_enough": admin.VERTICAL,
        "financial_status": admin.VERTICAL,
        "financial_status_compare": admin.VERTICAL,
        "household_debt": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
    }
