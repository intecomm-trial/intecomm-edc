from django.db import models
from edc_constants.constants import NOT_APPLICABLE
from edc_crf.model_mixins import SingletonCrfModelMixin
from edc_dx_review.model_mixins import (
    dx_initial_review_model_mixin_factory,
    rx_initial_review_model_mixin_factory,
)
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField

from intecomm_lists.models import HtnManagement

from ..choices import HTN_MANAGEMENT
from ..model_mixins import CrfModelMixin


class HtnInitialReview(
    dx_initial_review_model_mixin_factory("dx"),
    rx_initial_review_model_mixin_factory(
        "rx_init", verbose_name_label="medicines for hypertension"
    ),
    SingletonCrfModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    diagnosis_label = "hypertension"
    managed_by = models.ManyToManyField(
        HtnManagement,
        verbose_name="How is the patient's hypertension managed?",
    )

    managed_by_other = OtherCharField()

    managed_by_old = models.CharField(
        verbose_name="How is the patient's hypertension managed?",
        max_length=15,
        choices=HTN_MANAGEMENT,
        default=NOT_APPLICABLE,
        help_text="If patient is taking medication, complete the Drug Refill CRF.",
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Hypertension Initial Review"
        verbose_name_plural = "Hypertension Initial Reviews"
