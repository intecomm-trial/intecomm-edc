from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_adherence.model_mixins import (
    MedicationAdherenceModelMixin as BaseMedicationAdherenceModelMixin,
)
from edc_model_fields.fields import OtherCharField


class MedicationAdherenceModelMixin(BaseMedicationAdherenceModelMixin):
    condition_label = None

    meds_missed_in_days = models.IntegerField(
        verbose_name="In the last month, how many days did you miss taking your medication",
        validators=[MinValueValidator(1), MaxValueValidator(180)],
        null=True,
        blank=True,
    )

    meds_shortage_in_days = models.IntegerField(
        verbose_name="In the last month, how many days did you NOT HAVE medication to take",
        validators=[MinValueValidator(1), MaxValueValidator(180)],
        null=True,
        blank=True,
        help_text="That is, your supply of medication was finished",
    )

    meds_shortage_reason = models.ManyToManyField(
        "intecomm_lists.MedicationShortageReasons",
        verbose_name="Reasons for not having medications (supply/shortage)",
        blank=True,
    )

    meds_shortage_reason_other = OtherCharField(
        verbose_name="If `other` reason for not having medications, specify"
    )

    class Meta:
        abstract = True
