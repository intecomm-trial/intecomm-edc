from django import forms
from edc_constants.constants import DM, HIV, HTN, NO, OTHER, YES
from edc_crf.modelform_mixins import CrfSingletonModelFormMixin
from edc_form_validators import INVALID_ERROR, FormValidator

from ...constants import ALONE, PAID_WORK
from ...models import CareseekingA
from ..mixins import CrfModelFormMixin


class CareseekingAFormValidator(FormValidator):
    def clean(self) -> None:
        self.m2m_other_specify(m2m_field="med_conditions", field_other="med_conditions_other")
        self.applicable_if(
            NO, field="med_collected", field_applicable="med_not_collected_reason"
        )
        self.validate_other_specify(
            field="med_collected", other_specify_field="med_not_collected_reason_other"
        )
        self.required_if_m2m(HIV, field="med_conditions", field_required="med_cost_hiv")
        self.required_if_m2m(HTN, field="med_conditions", field_required="med_cost_htn")
        self.required_if_m2m(DM, field="med_conditions", field_required="med_cost_dm")

        self.applicable_if(YES, field="tests_requested", field_applicable="tests_done")
        self.applicable_if(NO, field="tests_done", field_applicable="tests_not_done_reason")
        self.validate_other_specify(
            field="tests_not_done_reason", other_specify_field="tests_not_done_other"
        )
        self.required_if(YES, field="tests_done", field_required="tests_cost")

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

        self.applicable_if(YES, field="referral", field_applicable="referral_type")
        self.applicable_if(YES, field="referral", field_applicable="referral_facility")

        self.m2m_single_selection_if(ALONE, m2m_field="accompany")
        if (
            self.cleaned_data.get("accompany_num")
            and ALONE in [o.name for o in self.cleaned_data.get("accompany")]
            and self.cleaned_data.get("accompany_num") != 0
        ):
            self.raise_validation_error(
                {"accompany_num": "Expected 0 based on response above"}, INVALID_ERROR
            )
        elif (
            self.cleaned_data.get("accompany_num")
            and ALONE not in [o.name for o in self.cleaned_data.get("accompany") or []]
            and self.cleaned_data.get("accompany_num") == 0
        ):
            self.raise_validation_error(
                {"accompany_num": "Expected a value greater than 0 based on response above"},
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
                {"money_source_main": "Response not found among responses given above"},
                INVALID_ERROR,
            )
        self.validate_other_specify(
            field="money_source_main", other_specify_field="money_source_main_other"
        )


class CareseekingAForm(
    CrfSingletonModelFormMixin,
    CrfModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = CareseekingAFormValidator

    class Meta:
        model = CareseekingA
        fields = "__all__"
