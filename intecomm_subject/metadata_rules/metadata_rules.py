from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.metadata_rules import CrfRule, CrfRuleGroup, P, register

from .predicates import Predicates

pc = Predicates()


@register()
class ClinicalReviewBaselineRuleGroup(CrfRuleGroup):

    hiv = CrfRule(
        predicate=P("hiv_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["hivinitialreview"],
    )

    diabetes = CrfRule(
        predicate=P("dm_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["dminitialreview"],
    )

    hypertension = CrfRule(
        predicate=P("htn_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["htninitialreview"],
    )

    class Meta:
        app_label = "intecomm_subject"
        source_model = "intecomm_subject.clinicalreviewbaseline"


@register()
class ClinicalReviewRuleGroup(CrfRuleGroup):

    hiv_dx = CrfRule(
        predicate=P("hiv_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["hivinitialreview"],
    )

    dm_dx = CrfRule(
        predicate=P("dm_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["dminitialreview"],
    )

    htn_dx = CrfRule(
        predicate=P("htn_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["htninitialreview"],
    )

    hiv_test = CrfRule(
        predicate=P("hiv_test", "eq", NOT_APPLICABLE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["hivreview"],
    )

    dm_test = CrfRule(
        predicate=P("dm_test", "eq", NOT_APPLICABLE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["dmreview"],
    )

    htn_test = CrfRule(
        predicate=P("htn_test", "eq", NOT_APPLICABLE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["htnreview"],
    )

    complications = CrfRule(
        predicate=P("complications", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["complicationsfollowup"],
    )

    class Meta:
        app_label = "intecomm_subject"
        source_model = "intecomm_subject.clinicalreview"


# @register()
# class FamilyHistoryRuleGroup(CrfRuleGroup):
#
#     family_history = CrfRule(
#         predicate=pc.family_history_required,
#         consequence=REQUIRED,
#         alternative=NOT_REQUIRED,
#         target_models=["familyhistory"],
#     )
#
#     class Meta:
#         app_label = "intecomm_subject"
#         source_model = "intecomm_subject.subjectvisit"


@register()
class MedicationsRuleGroup(CrfRuleGroup):

    refill_hiv = CrfRule(
        predicate=P("refill_hiv", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["drugrefillhiv"],
    )

    refill_dm = CrfRule(
        predicate=P("refill_dm", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["drugrefilldm"],
    )

    refill_htn = CrfRule(
        predicate=P("refill_htn", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["drugrefillhtn"],
    )

    adherence_hiv = CrfRule(
        predicate=P("refill_hiv", "in", [YES, NO]),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["hivmedicationadherence"],
    )

    adherence_dm = CrfRule(
        predicate=P("refill_dm", "in", [YES, NO]),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["dmmedicationadherence"],
    )

    adherence_htn = CrfRule(
        predicate=P("refill_htn", "in", [YES, NO]),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["htnmedicationadherence"],
    )

    class Meta:
        app_label = "intecomm_subject"
        source_model = "intecomm_subject.medications"
