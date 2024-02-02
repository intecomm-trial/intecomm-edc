from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin
from edc_visit_schedule.model_mixins import OnScheduleModelMixin


class OnScheduleInte(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):
    """A model used by the system. Auto-completed by subject_consent."""

    class Meta(OnScheduleModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "On-schedule facility-based integrated care"
        verbose_name_plural = "On-schedule facility-based integrated care"
        indexes = OnScheduleModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
