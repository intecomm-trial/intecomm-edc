from edc_adverse_event.pdf_reports import DeathReport as BaseDeathReport

from .pdf_report_mixin import ProtocolCrfReportMixin


class DeathReport(ProtocolCrfReportMixin, BaseDeathReport):

    pass
