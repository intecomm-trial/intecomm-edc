from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin, MedicationAdherenceModelMixin


class DmMedicationAdherence(
    MedicationAdherenceModelMixin,
    CrfModelMixin,
    edc_models.BaseUuidModel,
):

    condition_label = "Diabetes"

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Diabetes Medication Adherence"
        verbose_name_plural = "Diabetes Medication Adherence"
