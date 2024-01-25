from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import CLINIC, COMMUNITY
from edc_he.rule_groups import Predicates as BaseHealthEconomicsPredicates
from edc_visit_schedule.constants import MONTH12
from edc_visit_schedule.utils import is_baseline
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM
from intecomm_rando.utils import get_assignment_for_subject


class HealthEconomicsPredicates(BaseHealthEconomicsPredicates):
    pass


class LocationUpdatePredicates:
    @staticmethod
    def location_needs_update(visit, **kwargs) -> bool:
        required = False
        try:
            appt_type_name = visit.appointment.appt_type.name
        except AttributeError:
            pass
        else:
            if not is_baseline(visit):
                assignment = (
                    COMMUNITY
                    if get_assignment_for_subject(visit.subject_identifier) == COMMUNITY_ARM
                    else CLINIC
                )
                if assignment != appt_type_name:
                    required = True
        return required


class NextAppointmentPredicates:
    @staticmethod
    def is_required(visit, **kwargs) -> bool:
        return get_assignment_for_subject(visit.subject_identifier) == FACILITY_ARM


class ViralLoadPredicates:
    @staticmethod
    def is_required(visit, **kwargs) -> bool:
        model_cls = django_apps.get_model("intecomm_subject.hivinitialreview")
        try:
            model_cls.objects.get(subject_visit__subject_identifier=visit.subject_identifier)
        except ObjectDoesNotExist:
            is_required = False
        else:
            is_required = visit.visit_code == MONTH12
        return is_required
