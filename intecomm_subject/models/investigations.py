from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import NO
from edc_dx_review.models import ReasonsForTesting
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField

from ..model_mixins import CrfModelMixin


class Investigations(CrfModelMixin, BaseUuidModel):

    """Model not used"""

    hiv_tested = models.CharField(
        verbose_name="Was the patient tested for HIV infection?",
        max_length=15,
        choices=YES_NO,
        default=NO,
    )

    hypertension_tested = models.CharField(
        verbose_name="Was the patient tested for hypertension?",
        max_length=15,
        choices=YES_NO,
        default=NO,
    )

    diabetes_tested = models.CharField(
        verbose_name="Was the patient tested for diabetes?",
        max_length=15,
        choices=YES_NO,
        default=NO,
    )

    test_date = models.DateField(verbose_name="Date test requested", null=True, blank=True)

    reason = models.ManyToManyField(
        ReasonsForTesting, verbose_name="Why was the patient tested?", blank=True
    )

    reason_other = OtherCharField()

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Investigations"
        verbose_name_plural = "Investigations"
