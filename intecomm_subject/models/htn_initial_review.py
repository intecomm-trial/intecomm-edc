from django.db import models
from edc_constants.constants import NOT_APPLICABLE
from edc_dx_review.model_mixins.initial_review import InitialReviewModelMixin
from edc_model import duration_to_date
from edc_model.models import BaseUuidModel, DurationYMDField
from edc_model.validators import date_not_future
from edc_model_fields.fields import OtherCharField

from intecomm_lists.models import HtnManagement

from ..choices import HTN_MANAGEMENT
from ..model_mixins import CrfModelMixin


class HtnInitialReview(InitialReviewModelMixin, CrfModelMixin, BaseUuidModel):
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

    med_start_date = models.DateField(
        verbose_name="Medication start date, if known",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    med_start_ago = DurationYMDField(
        verbose_name=(
            "If the patient is taking medicines for hypertension, "
            "how long ago did they start taking these?"
        ),
        null=True,
        blank=True,
    )

    med_start_estimated_date = models.DateField(
        verbose_name="Estimated medication start date",
        null=True,
        editable=False,
        help_text="auto completed",
    )

    def save(self, *args, **kwargs):
        if self.med_start_ago:
            self.med_start_estimated_date = duration_to_date(
                self.med_start_ago, self.report_datetime
            )
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Hypertension Initial Review"
        verbose_name_plural = "Hypertension Initial Reviews"
