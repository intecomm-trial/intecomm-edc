from django.db import models
from edc_constants.choices import SMOKER_STATUS_SIMPLE, YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models
from edc_model import utils as edc_model_utils

from ..choices import ALCOHOL_CONSUMPTION, EDUCATION, EMPLOYMENT_STATUS, MARITAL_STATUS
from ..model_mixins import CrfModelMixin


class OtherBaselineData(CrfModelMixin, edc_models.BaseUuidModel):

    employment_status = models.CharField(
        verbose_name="What is the patient's employment status?",
        max_length=25,
        choices=EMPLOYMENT_STATUS,
    )

    employment_status_other = edc_models.OtherCharField()

    education = models.CharField(
        verbose_name="How much formal education does the patient have?",
        max_length=25,
        choices=EDUCATION,
    )

    marital_status = models.CharField(
        verbose_name="Personal status?",
        max_length=25,
        choices=MARITAL_STATUS,
    )

    smoking_status = models.CharField(
        verbose_name="Which of these options describes you",
        max_length=15,
        choices=SMOKER_STATUS_SIMPLE,
    )

    smoker_quit_ago = edc_models.DurationYMDField(
        verbose_name="If you used to smoke but stopped, how long ago did you stop",
        null=True,
        blank=True,
    )

    smoker_quit_estimated_date = models.DateField(
        verbose_name="Estimated date smoker quit?",
        null=True,
        editable=False,
    )

    alcohol = models.CharField(
        verbose_name="Do you drink alcohol?",
        max_length=15,
        choices=YES_NO,
    )

    alcohol_consumption = models.CharField(
        verbose_name="If yes, how often do you drink alcohol?",
        max_length=25,
        choices=ALCOHOL_CONSUMPTION,
        default=NOT_APPLICABLE,
    )

    def save(self, *args, **kwargs):
        if self.smoker_quit_ago:
            self.smoker_quit_estimated_date = edc_model_utils.duration_to_date(
                self.smoker_quit_ago, self.report_datetime
            )
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Other Baseline Data"
        verbose_name_plural = "Other Baseline Data"
