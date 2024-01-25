from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin
from edc_visit_schedule.model_mixins import OffScheduleModelMixin

from ..constants import OFFSCHEDULE_COMM_ACTION


class OffScheduleComm(SiteModelMixin, ActionModelMixin, OffScheduleModelMixin, BaseUuidModel):
    action_name = OFFSCHEDULE_COMM_ACTION
    offschedule_compare_dates_as_datetimes = False

    class Meta(OffScheduleModelMixin.Meta, ActionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Off-schedule community-based integrated care"
        verbose_name_plural = "Off-schedule community-based integrated care"
        indexes = (
            OffScheduleModelMixin.Meta.indexes
            + ActionModelMixin.Meta.indexes
            + BaseUuidModel.Meta.indexes
            + [
                models.Index(
                    fields=[
                        "id",
                        "subject_identifier",
                        "action_identifier",
                        "offschedule_datetime",
                        "site",
                    ]
                )
            ]
        )
