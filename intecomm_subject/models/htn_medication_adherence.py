from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin, MedicationAdherenceModelMixin


class HtnMedicationAdherence(
    MedicationAdherenceModelMixin,
    CrfModelMixin,
    edc_models.BaseUuidModel,
):

    condition_label = "Hypertension"

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Hypertension Medication Adherence"
        verbose_name_plural = "Hypertension Medication Adherence"
