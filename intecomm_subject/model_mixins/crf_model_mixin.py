from edc_crf.model_mixins import CrfModelMixin as BaseCrfModelMixin
from edc_crf.model_mixins import CrfStatusModelMixin


class CrfModelMixin(CrfStatusModelMixin, BaseCrfModelMixin):
    class Meta(CrfStatusModelMixin.Meta, BaseCrfModelMixin.Meta):
        abstract = True
        indexes = BaseCrfModelMixin.Meta.indexes
