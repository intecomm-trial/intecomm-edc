from edc_constants.constants import NOT_APPLICABLE, YES
from edc_he.rule_groups import HealthEconomicsRuleGroup as BaseHealthEconomicsRuleGroup
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.metadata_rules import CrfRule, CrfRuleGroup, P, register

from .predicates import (
    HealthEconomicsPredicates,
    LocationUpdatePredicates,
    MedicationAdherencePredicates,
    NextAppointmentPredicates,
)


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
    hiv_initial = CrfRule(
        predicate=P("hiv_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["hivinitialreview"],
    )

    dm_initial = CrfRule(
        predicate=P("dm_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["dminitialreview"],
    )

    htn_initial = CrfRule(
        predicate=P("htn_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["htninitialreview"],
    )

    hiv_review = CrfRule(
        predicate=P("hiv_test", "eq", NOT_APPLICABLE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["hivreview"],
    )

    dm_review = CrfRule(
        predicate=P("dm_test", "eq", NOT_APPLICABLE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["dmreview"],
    )

    htn_review = CrfRule(
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
        predicate="hiv_adherence_required",
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["hivmedicationadherence"],
    )

    adherence_dm = CrfRule(
        predicate="dm_adherence_required",
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["dmmedicationadherence"],
    )

    adherence_htn = CrfRule(
        predicate="htn_adherence_required",
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["htnmedicationadherence"],
    )

    class Meta:
        app_label = "intecomm_subject"
        source_model = "intecomm_subject.medications"
        predicates = MedicationAdherencePredicates()


@register()
class HealthEconomicsRuleGroup(BaseHealthEconomicsRuleGroup):
    class Meta:
        app_label = "intecomm_subject"
        source_model = "intecomm_subject.subjectvisit"
        predicates = HealthEconomicsPredicates()


@register()
class LocationUpdateRuleGroup(CrfRuleGroup):
    location_update = CrfRule(
        predicate="location_needs_update",
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["locationupdate"],
    )

    class Meta:
        app_label = "intecomm_subject"
        source_model = "intecomm_subject.subjectvisit"
        predicates = LocationUpdatePredicates()


@register()
class NextAppointmentRuleGroup(CrfRuleGroup):
    crf = CrfRule(
        predicate="is_required",
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["nextappointment"],
    )

    class Meta:
        app_label = "intecomm_subject"
        source_model = "intecomm_subject.subjectvisit"
        predicates = NextAppointmentPredicates()


@register()
class CareseekingRuleGroup(CrfRuleGroup):
    crfa = CrfRule(
        predicate="careseeking_required",
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["careseekinga"],
    )

    crfb = CrfRule(
        predicate="careseeking_required",
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["careseekingb"],
    )

    class Meta:
        app_label = "intecomm_subject"
        source_model = "intecomm_subject.subjectvisit"
        predicates = HealthEconomicsPredicates()
