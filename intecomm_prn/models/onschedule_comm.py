from edc_model.models import BaseUuidModel
from edc_sites.models import SiteModelMixin
from edc_visit_schedule.model_mixins import OnScheduleModelMixin


class OnScheduleComm(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):

    """A model used by the system. Auto-completed by subject_consent."""

    class Meta(OnScheduleModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "On-schedule community-based integrated care"
        verbose_name_plural = "On-schedule community-based integrated care"
        indexes = OnScheduleModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
