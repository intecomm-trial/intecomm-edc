from edc_crf.model_mixins import SingletonCrfModelMixin
from edc_he.model_mixins import PatientModelMixin
from edc_model.models import BaseUuidModel

from ...model_mixins import CrfModelMixin


class HealthEconomicsPatient(
    SingletonCrfModelMixin,
    PatientModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Health Economics: Patient"
        verbose_name_plural = "Health Economics: Patient"
