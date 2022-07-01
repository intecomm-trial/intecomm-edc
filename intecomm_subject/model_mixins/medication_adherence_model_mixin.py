from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from edc_model import models as edc_models

from intecomm_lists.models import NonAdherenceReasons
from intecomm_subject.choices import MISSED_PILLS


class MedicationAdherenceModelMixin(models.Model):

    condition_label = "condition_label"

    visual_score_slider = models.CharField(
        verbose_name=mark_safe(
            f"Visual adherence score for <U>{condition_label}</U> medication"
        ),
        max_length=3,
        help_text="%",
    )

    visual_score_confirmed = models.IntegerField(
        verbose_name=mark_safe(
            "<B><font color='orange'>Interviewer</font></B>: "
            "please confirm the score indicated from above."
        ),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="%",
    )

    last_missed_pill = models.CharField(
        verbose_name=mark_safe(
            "When was the last time you missed taking "
            f"your <U>{condition_label}</U> medication?"
        ),
        max_length=25,
        choices=MISSED_PILLS,
    )

    missed_pill_reason = models.ManyToManyField(
        NonAdherenceReasons,
        verbose_name="Reasons for miss taking medication",
        blank=True,
    )

    other_missed_pill_reason = edc_models.OtherCharField()

    class Meta:
        abstract = True
