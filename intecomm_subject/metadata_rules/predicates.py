from __future__ import annotations

from typing import TYPE_CHECKING

from edc_constants.constants import CLINIC, COMMUNITY
from edc_he.rule_groups import Predicates as BaseHealthEconomicsPredicates
from edc_visit_schedule.utils import is_baseline
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM
from intecomm_rando.utils import get_assignment_for_subject

if TYPE_CHECKING:
    from edc_metadata.model_mixins.creates import CreatesMetadataModelMixin
    from edc_visit_tracking.model_mixins import VisitModelMixin as Base

    class RelatedVisitModel(CreatesMetadataModelMixin, Base):
        pass


class HealthEconomicsPredicates(BaseHealthEconomicsPredicates):
    pass


class LocationUpdatePredicates:
    @staticmethod
    def location_needs_update(visit: RelatedVisitModel, **kwargs) -> bool:
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
    def is_required(visit: RelatedVisitModel, **kwargs) -> bool:
        return get_assignment_for_subject(visit.subject_identifier) == FACILITY_ARM
