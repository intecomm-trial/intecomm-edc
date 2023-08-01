from edc_crf.model_mixins import CrfStatusModelMixin
from edc_lab.model_mixins import RequisitionModelMixin
from edc_model.models import BaseUuidModel
from edc_reference.model_mixins import ReferenceModelMixin


class SubjectRequisition(
    RequisitionModelMixin, CrfStatusModelMixin, ReferenceModelMixin, BaseUuidModel
):
    class Meta(RequisitionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Subject requisition"
        verbose_name_plural = "Subject requisitions"
