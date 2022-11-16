from edc_action_item.models import ActionModelMixin
from edc_model.models import BaseUuidModel
from edc_sites.models import SiteModelMixin
from edc_visit_schedule.constants import OFFSCHEDULE_ACTION
from edc_visit_schedule.model_mixins import OffScheduleModelMixin


class OffScheduleFollowup(
    SiteModelMixin, ActionModelMixin, OffScheduleModelMixin, BaseUuidModel
):

    action_name = OFFSCHEDULE_ACTION
    offschedule_compare_dates_as_datetimes = False

    class Meta(OffScheduleModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Off-schedule Followup"
        verbose_name_plural = "Off-schedule Followup"
