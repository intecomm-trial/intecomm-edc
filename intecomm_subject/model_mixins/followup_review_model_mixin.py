from django.db import models
from edc_constants.constants import NOT_APPLICABLE

from intecomm_subject.choices import CARE_DELIVERY


class FollowupReviewModelMixin(models.Model):
    care_delivery = models.CharField(
        verbose_name="Care for this `condition` was delivered today at ...",
        max_length=25,
        choices=CARE_DELIVERY,
        default=NOT_APPLICABLE,
    )

    care_delivery_other = models.TextField(
        verbose_name="If other facility, please specify", null=True, blank=True
    )

    class Meta:
        abstract = True
