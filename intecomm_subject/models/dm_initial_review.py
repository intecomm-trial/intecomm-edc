from django.db import models
from edc_constants.choices import YES_NO
from edc_crf.model_mixins import SingletonCrfModelMixin
from edc_dx_review.model_mixins.factory import (
    dx_initial_review_model_mixin_factory,
    rx_initial_review_model_mixin_factory,
)
from edc_glucose.model_mixins import (
    fasting_model_mixin_factory,
    glucose_model_mixin_factory,
)
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField

from intecomm_lists.models import DmManagement

from ..model_mixins import CrfModelMixin


class DmInitialReview(
    dx_initial_review_model_mixin_factory("dx"),
    rx_initial_review_model_mixin_factory(
        "rx_init", verbose_name_label="medicines for diabetes"
    ),
    glucose_model_mixin_factory("glucose"),
    fasting_model_mixin_factory(
        "glucose",
        verbose_names=dict(
            glucose_fasting="Was glucose measured while fasting?",
            glucose_fasting_duration_str="How long did they fast (in hours and minutes)?",
        ),
    ),
    SingletonCrfModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    diagnosis_label = "diabetes"

    managed_by = models.ManyToManyField(
        DmManagement,
        verbose_name="How is the patient's diabetes managed?",
    )

    managed_by_other = OtherCharField()

    glucose_performed = models.CharField(
        verbose_name="Has the patient had their glucose measured in the last few months?",
        max_length=15,
        choices=YES_NO,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Diabetes Initial Review"
        verbose_name_plural = "Diabetes Initial Reviews"
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
