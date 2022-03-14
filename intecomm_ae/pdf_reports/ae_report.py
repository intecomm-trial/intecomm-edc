from edc_adverse_event.pdf_reports import AeReport as BaseAeReport

from .crf_report_mixin import CrfReportMixin


class AeReport(CrfReportMixin, BaseAeReport):

    pass
