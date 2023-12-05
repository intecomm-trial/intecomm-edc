from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_adverse_event.constants import AE_INITIAL_ACTION
from edc_adverse_event.model_mixins.ae_initial import (
    AeInitialFieldsModelMixin,
    AeInitialMethodsModelMixin,
)
from edc_adverse_event.models import AeClassification
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField
from edc_sites.model_mixins import SiteModelMixin

from ..pdf_reports import AePdfReport


class AeInitial(
    SiteModelMixin,
    ActionModelMixin,
    NonUniqueSubjectIdentifierFieldMixin,
    AeInitialFieldsModelMixin,
    AeInitialMethodsModelMixin,
    BaseUuidModel,
):
    action_name = AE_INITIAL_ACTION
    pdf_report_cls = AePdfReport

    ae_classification_as_text = models.CharField(
        verbose_name="Adverse Event (AE) Classification",
        max_length=150,
        null=True,
        blank=False,
        help_text="Keep this simple. Provide details below",
    )

    ae_classification = models.ForeignKey(
        AeClassification,
        on_delete=models.PROTECT,
        verbose_name="Adverse Event (AE) Classification",
        null=True,
        editable=False,
    )

    study_drug_relation = models.CharField(
        verbose_name="Relation to study drug:", max_length=25, null=True, editable=False
    )

    ae_classification_other = OtherCharField(max_length=250, null=True, editable=False)

    ae_treatment = models.TextField(verbose_name="Specify action taken for treatment of AE:")

    class Meta(
        NonUniqueSubjectIdentifierFieldMixin.Meta, ActionModelMixin.Meta, BaseUuidModel.Meta
    ):
        indexes = (
            NonUniqueSubjectIdentifierFieldMixin.Meta.indexes
            + ActionModelMixin.Meta.indexes
            + BaseUuidModel.Meta.indexes
        )
