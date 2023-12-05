from edc_crf.model_mixins import CrfStatusModelMixin
from edc_lab.model_mixins import RequisitionModelMixin
from edc_model.models import BaseUuidModel


class SubjectRequisition(RequisitionModelMixin, CrfStatusModelMixin, BaseUuidModel):
    class Meta(RequisitionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Subject requisition"
        verbose_name_plural = "Subject requisitions"
        indexes = RequisitionModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
