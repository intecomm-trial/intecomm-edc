from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

from edc_constants.constants import CLINIC, COMMUNITY, DM, HIV, HTN
from edc_dx import Diagnoses
from edc_dx.diagnoses import ClinicalReviewBaselineRequired, InitialReviewRequired
from edc_dx_review.constants import DIET_LIFESTYLE, DRUGS
from edc_he.rule_groups import Predicates as BaseHealthEconomicsPredicates
from edc_visit_schedule.constants import MONTH12
from edc_visit_schedule.utils import is_baseline
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM
from intecomm_rando.utils import get_assignment_for_subject

from intecomm_subject.models import HtnInitialReview, HtnReview

if TYPE_CHECKING:
    from edc_metadata.model_mixins.creates import CreatesMetadataModelMixin
    from edc_visit_tracking.model_mixins import VisitModelMixin as Base

    class RelatedVisitModel(CreatesMetadataModelMixin, Base):
        pass


class HealthEconomicsPredicates(BaseHealthEconomicsPredicates):
    @staticmethod
    def is_required_by_date(visit, **kwargs) -> bool:
        return visit.report_datetime >= datetime(2023, 7, 14, 1, 00, tzinfo=ZoneInfo("UTC"))

    @staticmethod
    def careseeking_required(visit, **kwargs) -> bool:
        """Returns True if after start date and 12m"""
        is_required_by_date = visit.report_datetime >= datetime(
            2024, 4, 22, 1, 00, tzinfo=ZoneInfo("UTC")
        )
        return is_required_by_date and visit.visit_code == MONTH12


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
        return (
            get_assignment_for_subject(visit.subject_identifier) == FACILITY_ARM
            and visit.visit_code != MONTH12
        )


class MedicationAdherencePredicates:
    @staticmethod
    def diagnoses(visit, **kwargs) -> list[str]:
        dxs = []
        try:
            diagnoses = Diagnoses(
                subject_identifier=visit.subject_identifier,
                report_datetime=visit.report_datetime,
                lte=True,
            )
        except ClinicalReviewBaselineRequired:
            pass
        else:
            try:
                dxs = [name for name in diagnoses.initial_reviews]
            except InitialReviewRequired:
                pass
        return dxs

    @staticmethod
    def is_required_by_date(visit, **kwargs) -> bool:
        return visit.report_datetime >= datetime(2023, 4, 19, 1, 00, tzinfo=ZoneInfo("UTC"))

    @staticmethod
    def is_required_by_date_hiv(visit, **kwargs) -> bool:
        return visit.report_datetime >= datetime(2023, 3, 22, 1, 00, tzinfo=ZoneInfo("UTC"))

    def hiv_adherence_required(self, visit, **kwargs) -> bool:

        return self.is_required_by_date_hiv and HIV.lower() in self.diagnoses(visit, **kwargs)

    def htn_adherence_required(self, visit, **kwargs) -> bool:
        # TODO: not required if managed_by for diet and lifestyle
        if (
            HtnInitialReview.objects.filter(
                subject_visit=visit, managed_by__name=DIET_LIFESTYLE
            )
            .exclude(managed_by__name=DRUGS)
            .exists()
            or HtnReview.objects.filter(subject_visit=visit, managed_by__name=DIET_LIFESTYLE)
            .exclude(managed_by__name=DRUGS)
            .exists()
        ):
            required = False
        else:
            required = self.is_required_by_date and HTN.lower() in self.diagnoses(
                visit, **kwargs
            )
        return required

    def dm_adherence_required(self, visit, **kwargs) -> bool:
        return self.is_required_by_date and DM.lower() in self.diagnoses(visit, **kwargs)
