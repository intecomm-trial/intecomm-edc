from edc_adverse_event.model_mixins import AeFollowupModelMixin
from edc_model.models.base_uuid_model import BaseUuidModel


class AeFollowup(AeFollowupModelMixin, BaseUuidModel):
    class Meta(AeFollowupModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "AE Followup"
        verbose_name_plural = "AE Followups"
        indexes = AeFollowupModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
