from edc_he.rule_groups import Predicates as BaseHealthEconomicsPredicates


class HealthEconomicsPredicates(BaseHealthEconomicsPredicates):
    app_label = "intecomm_subject"
    visit_model = "intecomm_subject.subjectvisit"
    assets_model = "intecomm_subject.healtheconomicsassets"
    household_head_model = "intecomm_subject.healtheconomicshouseholdhead"
    income_model = "intecomm_subject.healtheconomicsincome"
    patient_model = "intecomm_subject.healtheconomicspatient"
    property_model = "intecomm_subject.healtheconomicsproperty"
