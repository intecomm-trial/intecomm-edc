from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin, MedicationAdherenceModelMixin


class HivMedicationAdherence(
    MedicationAdherenceModelMixin,
    CrfModelMixin,
    edc_models.BaseUuidModel,
):

    condition_label = "HIV"

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "HIV Medication Adherence"
        verbose_name_plural = "HIV Medication Adherence"
