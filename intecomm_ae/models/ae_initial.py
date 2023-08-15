from django.db import models
from edc_adverse_event.model_mixins import AeInitialModelMixin
from edc_adverse_event.models import AeClassification
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField


class AeInitial(AeInitialModelMixin, BaseUuidModel):
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

    ae_classification_other = OtherCharField(max_length=250, null=True, editable=False)

    class Meta(AeInitialModelMixin.Meta, BaseUuidModel.Meta):
        pass
