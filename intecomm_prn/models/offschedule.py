from edc_identifier.managers import SubjectIdentifierManager
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_visit_schedule.model_mixins import CurrentSiteManager, OffScheduleModelMixin


class OffSchedule(OffScheduleModelMixin, BaseUuidModel):

    on_site = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    class Meta(OffScheduleModelMixin.Meta):
        pass


class OffSchedulePregnancy(OffScheduleModelMixin, BaseUuidModel):

    on_site = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    class Meta(OffScheduleModelMixin.Meta):
        pass
