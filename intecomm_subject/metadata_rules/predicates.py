from edc_he.rule_groups import Predicates as BaseHealthEconomicsPredicates
from edc_metadata.metadata_rules import PredicateCollection
from edc_visit_schedule.utils import is_baseline
from intecomm_rando.constants import FACILITY_ARM
from intecomm_rando.utils import get_assignment_for_subject


class HealthEconomicsPredicates(BaseHealthEconomicsPredicates):
    app_label = "intecomm_subject"
    visit_model = "intecomm_subject.subjectvisit"


class LocationUpdatePredicates(PredicateCollection):
    app_label = "intecomm_subject"
    visit_model = "intecomm_subject.subjectvisit"

    @staticmethod
    def location_needs_update(visit, **kwargs) -> bool:
        required = False
        try:
            appt_type_name = visit.appointment.appt_type.name
        except AttributeError:
            pass
        else:
            if not is_baseline(visit):
                assignment = get_assignment_for_subject(visit.subject_identifier)
                if assignment != appt_type_name:
                    required = True
        return required


class NextAppointmentPredicates(PredicateCollection):
    app_label = "intecomm_subject"
    visit_model = "intecomm_subject.subjectvisit"

    @staticmethod
    def is_required(visit, **kwargs) -> bool:
        return get_assignment_for_subject(visit.subject_identifier) == FACILITY_ARM
