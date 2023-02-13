from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import LIKERT_FREQUENCY, SMOKER_STATUS_SIMPLE, YES_NO
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
        verbose_name="Which of these options describes you?",
        max_length=15,
        choices=SMOKER_STATUS_SIMPLE,
    )

    smoker_quit_ago = DurationYMDField(
        verbose_name="If you used to smoke but stopped, how long ago did you stop?",
        null=True,
        blank=True,
    )

    smoker_current_duration = DurationYMDField(
        verbose_name="If you are still smoking, how long have you been smoking?",
        null=True,
        blank=True,
    )

    smoker_quit_estimated_date = models.DateField(
        verbose_name="Estimated date smoker quit?",
        null=True,
        editable=False,
    )

    smoker_current_duration_estimated_date = models.DateField(
        verbose_name="Estimated date smoker has been smoking since?",
        null=True,
        blank=True,
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

    activity_work = models.CharField(
        verbose_name=(
            "Does your work involve moderate or vigorous-intensity physical activity?"
        ),
        max_length=15,
        choices=YES_NO,
        help_text="See interviewer notes above.",
        null=True,
        blank=False,
    )

    activity_work_days_per_wk = models.IntegerField(
        verbose_name=(
            "If yes, how many DAYS do you do these physical activities as "
            "part of your work? (in a typical week)"
        ),
        validators=[MinValueValidator(0), MaxValueValidator(7)],
        blank=True,
        null=True,
        help_text="Number of days in a typical week",
    )

    activity_exercise_days_per_wk = models.IntegerField(
        verbose_name=(
            "How many DAYS do you do personal exercise, sports or fitness activities? "
            "(in a typical week)"
        ),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(7, message="Maximum days in a week is 7"),
        ],
        blank=True,
        null=True,
        help_text="Number of days in a typical week",
    )

    activity_combined_mn_avg_day = models.IntegerField(
        verbose_name=(
            "On an average day, how many MINUTES do you spend on all physical activities "
            "combined? (moderate or vigorous-intensity work activities, exercise, sports "
            "and fitness)"
        ),
        validators=[MinValueValidator(0), MaxValueValidator(1080)],
        blank=True,
        null=True,
        help_text="Number of minutes in a typical day",
    )

    num_leafy_vegs_eaten = models.IntegerField(
        verbose_name="On average, how many green leafy vegetables do you eat in a day?",
        help_text="Number per day",
    )

    num_other_vegs_eaten = models.IntegerField(
        verbose_name="On average, how many other vegetables do you eat in a day?",
        help_text="Other vegetables like carrots, tomatoes, bell papers etc. Number per day",
    )

    num_fruits_eaten = models.IntegerField(
        verbose_name="On average, how many vegetables do you eat in a day?",
        help_text="Number per day",
    )

    adds_salt_to_food = models.CharField(
        verbose_name=(
            "Do you add salt to your food in addition to what has been added when cooking?"
        ),
        max_length=15,
        choices=LIKERT_FREQUENCY,
        null=True,
        blank=False,
    )

    def save(self, *args, **kwargs):
        if self.smoker_quit_ago:
            self.smoker_quit_estimated_date = edc_model_utils.duration_to_date(
                self.smoker_quit_ago, self.report_datetime
            )
        if self.smoker_current_duration:
            self.smoker_current_duration_estimated_date = edc_model_utils.duration_to_date(
                self.smoker_current_duration, self.report_datetime
            )
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Other Baseline Data"
        verbose_name_plural = "Other Baseline Data"
