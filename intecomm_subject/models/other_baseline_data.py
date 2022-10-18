from django.db import models
from edc_constants.choices import SMOKER_STATUS_SIMPLE, YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_model import utils as edc_model_utils
from edc_model.models import BaseUuidModel, DurationYMDField
from edc_model_fields.fields import OtherCharField

from ..choices import ALCOHOL_CONSUMPTION, EDUCATION, EMPLOYMENT_STATUS, MARITAL_STATUS
from ..model_mixins import CrfModelMixin


class OtherBaselineData(CrfModelMixin, BaseUuidModel):

    employment_status = models.CharField(
        verbose_name="What is the patient's employment status?",
        max_length=25,
        choices=EMPLOYMENT_STATUS,
    )

    employment_status_other = OtherCharField()

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

    smoker_quit_ago = DurationYMDField(
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

    work_activity = models.CharField(
        verbose_name="Does your work involve moderate or vigorous-intensity activity that"
        "causes small to large increases in breathing or heart rate like "
        "carrying or lifting loads, digging or construction work",
        max_length=15,
        choices=YES_NO,
    )
    work_activity_days = models.IntegerField(
        verbose_name="In a typical week, how many days do you do these moderate or "
        "vigorous-intensity activities as part of your work?",
        blank=True,
        null=True,
        help_text="Give number of days in a 7-day week",
    )

    work_activity_exercise = models.IntegerField(
        verbose_name="In addition to the moderate or vigorous-intensity activity above, "
        "how many days do you do exercise, do sports or fitness activities in a "
        "typical week?",
        blank=True,
        null=True,
        help_text="Give number of days in a 7-day week",
    )
    work_activity_exercise_time = models.IntegerField(
        verbose_name="On an average day, how long do you spend combined on the moderate or "
        "vigorous-intensity activities and doing exercise, sports and fitness "
        "activities?",
        blank=True,
        null=True,
        help_text="Give number of minutes",
    )

    num_vegetables_eaten = models.IntegerField(
        verbose_name="On average, how many vegetables do you eat in a day?"
    )

    use_salt_on_food = models.CharField(
        verbose_name="Do you add salt to your food in addition to what has been added when "
        "cooking?",
        max_length=15,
        choices=YES_NO,
    )

    def save(self, *args, **kwargs):
        if self.smoker_quit_ago:
            self.smoker_quit_estimated_date = edc_model_utils.duration_to_date(
                self.smoker_quit_ago, self.report_datetime
            )
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Other Baseline Data"
        verbose_name_plural = "Other Baseline Data"
