from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from edc_constants.constants import BOTH, NO, NOT_APPLICABLE, OUTPATIENT, YES
from edc_crf.crf_form_validator_mixins import CrfFormValidatorMixin
from edc_crf.modelform_mixins import CrfSingletonModelFormMixin
from edc_dx import Diagnoses, get_diagnosis_labels
from edc_form_validators import INVALID_ERROR, FormValidator

from ...choices import ACCOMPANIED_BY, TRAVEL_METHODS
from ...constants import ALONE
from ...models import CareseekingA, CareseekingB
from ..mixins import CrfModelFormMixin


class CareseekingBFormValidator(CrfFormValidatorMixin, FormValidator):
    def clean(self) -> None:
        try:
            CareseekingA.objects.get(subject_visit__subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                f"Please complete form {CareseekingA._meta.verbose_name} first."
            )
        care_seeking_b = CareseekingB.objects.filter(
            subject_visit__subject_identifier=self.related_visit.subject_identifier
        ).exclude(subject_visit_id=self.related_visit.id)
        if care_seeking_b.count() > 0:
            raise forms.ValidationError(
                f"This form has already been submitted. See {care_seeking_b[0].subject_visit}."
            )

        # B1:
        self.applicable_if(YES, field="needed_care", field_applicable="accessed_care")
        self.applicable_if(NO, field="accessed_care", field_applicable="no_accessed_care")
        self.validate_other_specify(
            field="no_accessed_care", other_specify_field="no_accessed_care_other"
        )
        self.applicable_if(YES, field="accessed_care", field_applicable="seek_facility")
        self.validate_other_specify(
            field="accessed_care", other_specify_field="accessed_care_other"
        )
        self.applicable_if(YES, field="accessed_care", field_applicable="care_type")
        self.required_if(
            OUTPATIENT,
            BOTH,
            field="care_type",
            field_required="outpatient_visits",
            field_required_evaluate_as_int=True,
        )

        # B2: Travel and expenses at last/most recent visit
        self.m2m_required_if(YES, field="accessed_care", m2m_field="travel_method")
        self.required_if_m2m(
            *[t[0] for t in TRAVEL_METHODS],
            field="travel_method",
            field_required="travel_duration",
            field_other_evaluate_as_int=True,
        )
        self.required_if_m2m(
            *[t[0] for t in TRAVEL_METHODS],
            field="travel_method",
            field_required="travel_costs",
            field_other_evaluate_as_int=True,
        )
        self.required_if_m2m(
            *[t[0] for t in TRAVEL_METHODS],
            field="travel_method",
            field_required="food_costs",
            field_other_evaluate_as_int=True,
        )
        self.required_if(
            YES,
            field="accessed_care",
            field_required="care_costs",
            field_required_evaluate_as_int=True,
        )

        # B3: Medications at last/most recent visit
        self.applicable_if(YES, field="accessed_care", field_applicable="med_prescribed")
        self.m2m_required_if(YES, field="med_prescribed", m2m_field="med_conditions")
        med_conditions = self.cleaned_data.get("med_conditions")
        diagnoses = Diagnoses(
            subject_identifier=self.subject_identifier,
            report_datetime=self.report_datetime,
            lte=True,
        )
        if invalid_conditions := set([o.name.lower() for o in med_conditions or []]) - set(
            diagnoses.initial_reviews
        ):
            if labels := ", ".join(
                [
                    get_diagnosis_labels().get(label)
                    for label in invalid_conditions
                    if label in get_diagnosis_labels()
                ]
            ):
                self.raise_validation_error(
                    {
                        "med_conditions": (
                            f"Subject has not been diagnosed with these conditions: {labels}"
                        )
                    },
                    INVALID_ERROR,
                )

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

        # B4: Tests at last/most recent visit
        self.applicable_if(YES, field="accessed_care", field_applicable="tests_requested")
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

        # B5: Time and expenses at last/most recent visit
        self.required_if(YES, field="accessed_care", field_required="care_visit_duration")
        self.applicable_if(YES, field="accessed_care", field_applicable="missed_activities")
        self.validate_other_specify(
            field="missed_activities", other_specify_field="missed_activities_other"
        )

        # B6: People who accompanied you to last/most recent visit
        self.applicable_if(YES, field="accessed_care", field_applicable="accompany")
        self.required_if(
            *[t[0] for t in ACCOMPANIED_BY if t[0] not in [ALONE, NOT_APPLICABLE]],
            field="accompany",
            field_required="accompany_num",
        )
        self.applicable_if(
            *[t[0] for t in ACCOMPANIED_BY if t[0] not in [ALONE, NOT_APPLICABLE]],
            field="accompany",
            field_applicable="accompany_wait",
        )
        self.applicable_if(
            *[t[0] for t in ACCOMPANIED_BY if t[0] not in [ALONE, NOT_APPLICABLE]],
            field="accompany",
            field_applicable="accompany_alt",
        )
        self.validate_other_specify(
            field="accompany_alt", other_specify_field="accompany_alt_other"
        )

        # B7: Your expenses in the past 3 months
        self.m2m_required_if(YES, field="accessed_care", m2m_field="money_sources")
        money_sources = [o.name for o in self.cleaned_data.get("money_sources")]
        if len(money_sources) > 3:
            self.raise_validation_error(
                {"money_sources": "Please limit to no more than 3 selections"}, INVALID_ERROR
            )
        self.m2m_other_specify(m2m_field="money_sources", field_other="money_sources_other")
        self.applicable_if(YES, field="accessed_care", field_applicable="money_source_main")
        if (
            self.cleaned_data.get("money_source_main")
            and money_sources
            and self.cleaned_data.get("money_source_main") not in money_sources
        ):
            self.raise_validation_error(
                {"money_source_main": _("Response not found among responses given above")},
                INVALID_ERROR,
            )
        # B8: About your inpatient visit
        self.required_if(YES, field="inpatient", field_required="inpatient_days")
        self.m2m_required_if(YES, field="inpatient", m2m_field="inpatient_reasons")
        self.m2m_other_specify(
            m2m_field="inpatient_reasons", field_other="inpatient_reasons_other"
        )

        # B9: Inpatient visit: expenses
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

        # B10: Inpatient visit: sources of payment for expenses
        self.m2m_required_if(YES, field="inpatient", m2m_field="inpatient_money_sources")
        inpatient_money_sources = [
            o.name for o in self.cleaned_data.get("inpatient_money_sources")
        ]
        if len(inpatient_money_sources) > 3:
            self.raise_validation_error(
                {"inpatient_money_sources": "Please limit to no more than 3 selections"},
                INVALID_ERROR,
            )
        self.m2m_other_specify(
            m2m_field="inpatient_money_sources", field_other="inpatient_money_sources_other"
        )
        self.applicable_if(
            YES, field="inpatient", field_applicable="inpatient_money_sources_main"
        )
        if (
            self.cleaned_data.get("inpatient_money_sources_main")
            and inpatient_money_sources
            and self.cleaned_data.get("inpatient_money_sources_main")
            not in [o.name for o in self.cleaned_data.get("inpatient_money_sources")]
        ):
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
