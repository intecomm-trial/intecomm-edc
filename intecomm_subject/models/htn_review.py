from django.db import models
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import BaseUuidModel
from edc_vitals.models import DiastolicPressureField, SystolicPressureField

from intecomm_subject.choices import HTN_MANAGEMENT

from ..model_mixins import CrfModelMixin, FollowupReviewModelMixin


class HtnReview(FollowupReviewModelMixin, CrfModelMixin, BaseUuidModel):

    test_date = models.DateField(
        verbose_name="Date tested for Hypertension",
        null=True,
        blank=True,
        editable=False,
        help_text="",
    )

    dx = models.CharField(
        verbose_name="Has the patient been diagnosed with Hypertension?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    sys_blood_pressure = SystolicPressureField(null=True, blank=True)

    dia_blood_pressure = DiastolicPressureField(null=True, blank=True)

    managed_by = models.CharField(
        verbose_name="How will the patient's hypertension be managed going forward?",
        max_length=25,
        choices=HTN_MANAGEMENT,
        default=NOT_APPLICABLE,
    )

    care_start_date = models.DateField(
        verbose_name="Date clinical management started",
        null=True,
        blank=True,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Hypertension Review"
        verbose_name_plural = "Hypertension Review"
