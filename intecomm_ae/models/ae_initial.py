from edc_adverse_event.model_mixins import AeInitialModelMixin
from edc_model.models import BaseUuidModel


class AeInitial(AeInitialModelMixin, BaseUuidModel):
    class Meta(AeInitialModelMixin.Meta, BaseUuidModel.Meta):
        pass
