from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin, MedicationAdherenceModelMixin


class HivMedicationAdherence(
    MedicationAdherenceModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    condition_label = "HIV"

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Medication Adherence (HIV)"
        verbose_name_plural = "Medication Adherence (HIV)"
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
