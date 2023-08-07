from edc_he.rule_groups import Predicates as BaseHealthEconomicsPredicates


class HealthEconomicsPredicates(BaseHealthEconomicsPredicates):
    app_label = "intecomm_subject"
    visit_model = "intecomm_subject.subjectvisit"
