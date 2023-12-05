from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin, MedicationAdherenceModelMixin


class DmMedicationAdherence(
    MedicationAdherenceModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    condition_label = "Diabetes"

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Medication Adherence (Diabetes)"
        verbose_name_plural = "Medication Adherence (Diabetes)"
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
