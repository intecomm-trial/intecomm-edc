from edc_action_item.models import ActionModelMixin
from edc_model.models import BaseUuidModel
from edc_sites.models import SiteModelMixin
from edc_visit_schedule.model_mixins import OffScheduleModelMixin

from ..constants import OFFSCHEDULE_INTE_ACTION


class OffScheduleInte(SiteModelMixin, ActionModelMixin, OffScheduleModelMixin, BaseUuidModel):
    action_name = OFFSCHEDULE_INTE_ACTION
    offschedule_compare_dates_as_datetimes = False

    class Meta(OffScheduleModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Off-schedule Facility Integrated Care"
        verbose_name_plural = "Off-schedule Facility Integrated Care"
