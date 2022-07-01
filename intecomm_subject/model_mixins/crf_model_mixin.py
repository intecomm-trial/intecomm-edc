from edc_crf.crf_status_model_mixin import CrfStatusModelMixin
from edc_crf.crf_model_mixin import CrfModelMixin as BaseCrfModelMixin


class CrfModelMixin(CrfStatusModelMixin, BaseCrfModelMixin):
    class Meta(BaseCrfModelMixin.Meta):
        abstract = True
