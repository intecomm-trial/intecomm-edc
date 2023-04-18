from edc_action_item.models import ActionModelMixin
from edc_model.models import BaseUuidModel
from edc_sites.models import SiteModelMixin
from edc_visit_schedule.model_mixins import OffScheduleModelMixin

from ..constants import OFFSCHEDULE_COMM_ACTION


class OffScheduleComm(SiteModelMixin, ActionModelMixin, OffScheduleModelMixin, BaseUuidModel):
    action_name = OFFSCHEDULE_COMM_ACTION
    offschedule_compare_dates_as_datetimes = False

    class Meta(OffScheduleModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Off-schedule Community Integrated Care"
        verbose_name_plural = "Off-schedule Community Integrated Care"
