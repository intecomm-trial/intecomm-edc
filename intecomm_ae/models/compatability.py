"""These models are not used by this trial. They are added to
maintain compatability with edc_adverse_event.
"""

from edc_adverse_event.model_mixins import (
    AeSusarModelMixin,
    AeTmgModelMixin,
    DeathReportTmgModelMixin,
)
from edc_model.models import BaseUuidModel


class AeSusar(AeSusarModelMixin, BaseUuidModel):
    class Meta(AeSusarModelMixin.Meta, BaseUuidModel.Meta):
        indexes = AeSusarModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes


class AeTmg(AeTmgModelMixin, BaseUuidModel):
    class Meta(AeTmgModelMixin.Meta, BaseUuidModel.Meta):
        indexes = AeTmgModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes


class DeathReportTmg(DeathReportTmgModelMixin, BaseUuidModel):
    class Meta(DeathReportTmgModelMixin.Meta, BaseUuidModel.Meta):
        indexes = DeathReportTmgModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes


class DeathReportTmgSecond(DeathReportTmg):
    class Meta:
        proxy = True
