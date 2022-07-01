from django.db import models
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class Medications(CrfModelMixin, edc_models.BaseUuidModel):

    refill_hiv = models.CharField(
        verbose_name="Is the patient filling / refilling HIV medications?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=(
            "Select `not applicable` if subject has not "
            "been diagnosed and prescribed medication for HIV infection."
        ),
    )

    refill_dm = models.CharField(
        verbose_name="Is the patient filling / refilling Diabetes medications?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=(
            "Select `not applicable` if subject has not "
            "been diagnosed and prescribed medication for Diabetes."
        ),
    )

    refill_htn = models.CharField(
        verbose_name="Is the patient filling / refilling Hypertension medications?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=(
            "Select `not applicable` if subject has not "
            "been diagnosed and prescribed medication for Hypertension."
        ),
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Medications"
        verbose_name_plural = "Medications"
