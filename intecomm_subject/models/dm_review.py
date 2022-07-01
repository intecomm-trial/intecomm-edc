from django.db import models
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models

from intecomm_subject.choices import DM_MANAGEMENT

from ..model_mixins import CrfModelMixin, GlucoseModelMixin, ReviewModelMixin


class DmReview(ReviewModelMixin, GlucoseModelMixin, CrfModelMixin, edc_models.BaseUuidModel):

    test_date = models.DateField(
        verbose_name="Date tested for diabetes",
        null=True,
        blank=True,
        help_text="QUESTION_RETIRED",
        editable=False,
    )

    dx = models.CharField(
        verbose_name="Has the patient been diagnosed with Diabetes?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="QUESTION_RETIRED",
        editable=False,
    )

    managed_by = models.CharField(
        verbose_name="How will the patient's diabetes be managed going forward?",
        max_length=25,
        choices=DM_MANAGEMENT,
        default=NOT_APPLICABLE,
    )

    care_start_date = models.DateField(
        verbose_name="Date clinical management started",
        null=True,
        blank=False,
        help_text="QUESTION_RETIRED",
        editable=False,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Diabetes Review"
        verbose_name_plural = "Diabetes Review"
