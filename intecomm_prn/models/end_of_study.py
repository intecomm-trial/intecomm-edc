from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_constants.constants import CLINICAL_WITHDRAWAL, DEAD, NOT_APPLICABLE, OTHER
from edc_ltfu.constants import LOST_TO_FOLLOWUP
from edc_model.models import BaseUuidModel
from edc_model.validators import date_not_future
from edc_offstudy.constants import (
    COMPLETED_FOLLOWUP,
    CONSENT_WITHDRAWAL,
    END_OF_STUDY_ACTION,
)
from edc_offstudy.model_mixins import OffstudyModelMixin
from edc_sites.models import SiteModelMixin
from edc_transfer.constants import TRANSFERRED

from intecomm_lists.models import OffstudyReasons

from ..choices import CLINICAL_WITHDRAWAL_REASONS


class EndOfStudy(SiteModelMixin, ActionModelMixin, OffstudyModelMixin, BaseUuidModel):

    action_name = END_OF_STUDY_ACTION

    tracking_identifier_prefix = "ST"

    last_seen_date = models.DateField(
        verbose_name="Date patient was last seen",
        validators=[date_not_future],
        blank=False,
        null=True,
    )

    offstudy_reason = models.ForeignKey(
        OffstudyReasons,
        verbose_name="Reason patient was terminated from the study",
        on_delete=models.PROTECT,
        null=True,
        limit_choices_to={
            "name__in": [
                COMPLETED_FOLLOWUP,
                CONSENT_WITHDRAWAL,
                CLINICAL_WITHDRAWAL,
                LOST_TO_FOLLOWUP,
                TRANSFERRED,
                DEAD,
                OTHER,
            ]
        },
    )

    other_offstudy_reason = models.TextField(
        verbose_name="If OTHER, please specify", max_length=500, blank=True, null=True
    )

    clinical_withdrawal_reason = models.CharField(
        verbose_name=(
            "If the patient was withdrawn on CLINICAL grounds, "
            "please specify PRIMARY reason"
        ),
        max_length=25,
        choices=CLINICAL_WITHDRAWAL_REASONS,
        default=NOT_APPLICABLE,
    )

    clinical_withdrawal_reason_other = models.TextField(
        verbose_name="If withdrawn for 'other' condition, please explain",
        max_length=500,
        blank=True,
        null=True,
    )

    clinical_withdrawal_investigator_decision = models.TextField(
        verbose_name="If withdrawl was an 'investigator decision', please explain ...",
        max_length=500,
        blank=True,
        null=True,
    )

    ltfu_date = models.DateField(
        verbose_name="Date lost to followup, if applicable",
        validators=[date_not_future],
        blank=True,
        null=True,
        help_text="A Loss to followup report must be on file",
    )

    transfer_date = models.DateField(
        verbose_name="Date of transfer, if applicable",
        validators=[date_not_future],
        blank=True,
        null=True,
        help_text="A Transfer form must be on file.",
    )

    death_date = models.DateField(
        verbose_name="Date of death, if applicable",
        validators=[date_not_future],
        blank=True,
        null=True,
        help_text="A Death report must be on file",
    )

    comment = models.TextField(
        verbose_name="Please provide further details if possible",
        max_length=500,
        blank=True,
        null=True,
    )

    class Meta(OffstudyModelMixin.Meta):
        verbose_name = "End of Study"
        verbose_name_plural = "End of Study"
