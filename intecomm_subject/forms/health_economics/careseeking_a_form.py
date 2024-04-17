from django import forms
from edc_constants.constants import DM, HIV, HTN, NO, OTHER, YES
from edc_crf.crf_form_validator_mixins import CrfFormValidatorMixin
from edc_crf.modelform_mixins import CrfSingletonModelFormMixin
from edc_form_validators import INVALID_ERROR, FormValidator

from ...constants import ADULT, CHILD, MAIN_EARNER, STUDY_VISIT
from ...models import CareseekingA
from ..mixins import CrfModelFormMixin


class CareseekingAFormValidator(CrfFormValidatorMixin, FormValidator):
    def clean(self) -> None:
        care_seeking_a = CareseekingA.objects.filter(
            subject_visit__subject_identifier=self.related_visit.subject_identifier
        ).exclude(subject_visit_id=self.related_visit.id)
        if care_seeking_a.count() > 0:
            raise forms.ValidationError(
                f"This form has already been submitted. See {care_seeking_a[0].subject_visit}."
            )
        self.m2m_single_selection_if(STUDY_VISIT, m2m_field="care_visit_reason")

        self.m2m_other_specify(
            m2m_field="care_visit_reason", field_other="care_visit_reason_other"
        )

        # A3: Medication costs for today's visit
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

        med_conditions = [o.name for o in self.cleaned_data.get("med_conditions")]
        med_cost_tot = self.cleaned_data.get("med_cost_tot")
        self.required_if(
            YES,
            field="med_collected",
            field_required="med_cost_tot",
            field_required_evaluate_as_int=True,
        )
        self.required_if_true(
            HIV in med_conditions and med_cost_tot is not None and med_cost_tot > 0,
            field_required="med_cost_hiv",
        )
        self.required_if_true(
            HTN in med_conditions and med_cost_tot is not None and med_cost_tot > 0,
            field_required="med_cost_htn",
        )
        self.required_if_true(
            DM in med_conditions and med_cost_tot is not None and med_cost_tot > 0,
            field_required="med_cost_dm",
        )
        self.required_if_true(
            OTHER in med_conditions and med_cost_tot is not None and med_cost_tot > 0,
            field_required="med_cost_other",
        )
        self.applicable_if(
            YES, field="med_collected", field_applicable="med_collected_location"
        )
        self.validate_other_specify(
            field="med_collected_location", other_specify_field="med_collected_location_other"
        )

        # A4: Diagnostic costs for today's visit
        self.applicable_if(YES, field="tests_requested", field_applicable="tests_done")
        self.applicable_if(NO, field="tests_done", field_applicable="tests_not_done_reason")
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

        self.applicable_if(YES, field="referral", field_applicable="referral_type")
        self.applicable_if(YES, field="referral", field_applicable="referral_facility")

        # accompany
        self.required_if(
            ADULT,
            CHILD,
            MAIN_EARNER,
            field="accompany",
            field_required="accompany_num",
            field_required_evaluate_as_int=True,
        )
        self.applicable_if_true(
            self.cleaned_data.get("accompany_num")
            and self.cleaned_data.get("accompany_num") > 0,
            field_applicable="accompany_wait",
        )
        self.applicable_if_true(
            self.cleaned_data.get("accompany_num")
            and self.cleaned_data.get("accompany_num") > 0,
            field_applicable="accompany_alt",
        )
        self.validate_other_specify(
            field="accompany_alt", other_specify_field="accompany_alt_other"
        )

        # A8: Your expenses for today's visit / money_sources
        money_sources = [o.name for o in self.cleaned_data.get("money_sources") or []]
        if len(money_sources) > 3:
            self.raise_validation_error(
                {"money_sources": "Please limit to no more than 3 selections"}, INVALID_ERROR
            )
        self.m2m_other_specify(m2m_field="money_sources", field_other="money_sources_other")

        if self.cleaned_data.get("money_source_main") and self.cleaned_data.get(
            "money_source_main"
        ) not in [o.name for o in self.cleaned_data.get("money_sources") or []]:
            self.raise_validation_error(
                {"money_source_main": "Response not found among responses given above"},
                INVALID_ERROR,
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
