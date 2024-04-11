from django import forms
from django.utils.translation import gettext as _
from edc_constants.constants import BOTH, NO, OTHER, OUTPATIENT, YES
from edc_crf.modelform_mixins import CrfSingletonModelFormMixin
from edc_form_validators import INVALID_ERROR, FormValidator

from ...constants import ALONE, PAID_WORK
from ...models import CareseekingB
from ..mixins import CrfModelFormMixin


class CareseekingBFormValidator(FormValidator):
    def clean(self) -> None:
        self.applicable_if(YES, field="ill_month", field_applicable="seek_advice")
        self.applicable_if(NO, field="seek_advice", field_applicable="no_seek_advice")
        self.validate_other_specify(
            field="no_seek_advice", other_specify_field="no_seek_advice_other"
        )
        self.applicable_if(YES, field="seek_advice", field_applicable="seek_facility")
        self.validate_other_specify(
            field="seek_advice", other_specify_field="seek_advice_other"
        )
        self.applicable_if(YES, field="seek_advice", field_applicable="seek_care_type")
        self.required_if(
            OUTPATIENT,
            BOTH,
            field="seek_care_type",
            field_required="outpatient_visits",
            field_required_evaluate_as_int=True,
        )

        self.m2m_required_if(YES, field="med_prescribed", m2m_field="med_conditions")
        self.m2m_other_specify(m2m_field="med_conditions", field_other="med_conditions_other")
        self.applicable_if(YES, field="med_prescribed", field_applicable="med_collected")
        self.applicable_if(
            NO, field="med_collected", field_applicable="med_not_collected_reason"
        )
        self.validate_other_specify(
            field="med_not_collected_reason",
            other_specify_field="med_not_collected_reason_other",
        )
        self.required_if(
            YES,
            field="med_collected",
            field_required="med_cost_tot",
            field_required_evaluate_as_int=True,
        )

        self.applicable_if(YES, field="tests_requested", field_applicable="tests_done")
        self.required_if(NO, field="tests_done", field_required="tests_not_done_reason")
        self.validate_other_specify(
            field="tests_not_done_reason", other_specify_field="tests_not_done_other"
        )
        self.required_if(
            YES,
            field="tests_done",
            field_required="tests_cost",
            field_required_evaluate_as_int=True,
        )

        self.validate_other_specify(
            field="missed_activities", other_specify_field="missed_activities_other"
        )
        self.required_if(
            PAID_WORK,
            OTHER,
            field="missed_activities",
            field_required="care_visit_lost_income",
            field_required_evaluate_as_int=True,
        )

        self.m2m_single_selection_if(ALONE, m2m_field="accompany")
        if (
            self.cleaned_data.get("accompany_num")
            and ALONE in [o.name for o in self.cleaned_data.get("accompany")]
            and self.cleaned_data.get("accompany_num") != 0
        ):
            self.raise_validation_error(
                {"accompany_num": _("Expected 0 based on response above")}, INVALID_ERROR
            )
        elif (
            self.cleaned_data.get("accompany_num")
            and ALONE not in [o.name for o in self.cleaned_data.get("accompany") or []]
            and self.cleaned_data.get("accompany_num") == 0
        ):
            self.raise_validation_error(
                {
                    "accompany_num": _(
                        "Expected a value greater than 0 based on response above"
                    )
                },
                INVALID_ERROR,
            )

        self.applicable_if_true(
            ALONE not in [o.name for o in self.cleaned_data.get("accompany") or []],
            field_applicable="accompany_wait",
        )
        self.applicable_if_true(
            ALONE not in [o.name for o in self.cleaned_data.get("accompany") or []],
            field_applicable="accompany_alt",
        )
        self.validate_other_specify(
            field="accompany_alt", other_specify_field="accompany_alt_other"
        )
        self.required_if(
            PAID_WORK,
            OTHER,
            field="accompany_alt",
            field_required="accompany_lost_income",
            field_required_evaluate_as_int=True,
        )

        self.m2m_other_specify(m2m_field="money_sources", field_other="money_sources_other")

        if self.cleaned_data.get("money_source_main") and self.cleaned_data.get(
            "money_source_main"
        ) not in [o.name for o in self.cleaned_data.get("money_sources")]:
            self.raise_validation_error(
                {"money_source_main": _("Response not found among responses given above")},
                INVALID_ERROR,
            )
        self.validate_other_specify(
            field="money_source_main", other_specify_field="money_source_main_other"
        )

        self.required_if(YES, field="inpatient", field_required="inpatient_days")
        self.m2m_required_if(YES, field="inpatient", m2m_field="inpatient_reasons")
        self.m2m_other_specify(
            m2m_field="inpatient_reasons", field_other="inpatient_reasons_other"
        )
        self.required_if(
            YES,
            field="inpatient",
            field_required="inpatient_cost",
            field_required_evaluate_as_int=True,
        )
        self.required_if(YES, field="inpatient", field_required="inpatient_accompany")
        self.required_if(YES, field="inpatient", field_required="inpatient_food")
        self.required_if(
            YES,
            field="inpatient_food",
            field_required="inpatient_food_cost",
            field_required_evaluate_as_int=True,
        )
        self.required_if(
            YES,
            field="inpatient",
            field_required="inpatient_nowork_days",
            field_required_evaluate_as_int=True,
        )
        self.required_if(YES, field="inpatient", field_required="inpatient_household_nowork")
        self.required_if(
            YES,
            field="inpatient_household_nowork",
            field_required="inpatient_household_nowork_days",
            field_required_evaluate_as_int=True,
        )

        self.m2m_other_specify(
            m2m_field="inpatient_money_sources", field_other="inpatient_money_sources_other"
        )

        if self.cleaned_data.get("inpatient_money_sources_main") and self.cleaned_data.get(
            "inpatient_money_sources_main"
        ) not in [o.name for o in self.cleaned_data.get("inpatient_money_sources")]:
            self.raise_validation_error(
                {
                    "inpatient_money_sources_main": _(
                        "Response not found among responses given above"
                    )
                },
                INVALID_ERROR,
            )
        self.validate_other_specify(
            field="inpatient_money_sources_main",
            other_specify_field="inpatient_money_sources_main_other",
        )


class CareseekingBForm(
    CrfSingletonModelFormMixin,
    CrfModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = CareseekingBFormValidator

    class Meta:
        model = CareseekingB
        fields = "__all__"
