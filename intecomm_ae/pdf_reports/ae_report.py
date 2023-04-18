from edc_adverse_event.pdf_reports import AeReport as BaseAeReport

from .pdf_report_mixin import ProtocolCrfReportMixin


class AeReport(ProtocolCrfReportMixin, BaseAeReport):
    pass
