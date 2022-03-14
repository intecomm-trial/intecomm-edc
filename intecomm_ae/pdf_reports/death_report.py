from edc_adverse_event.pdf_reports import DeathReport as BaseDeathReport

from .crf_report_mixin import CrfReportMixin


class DeathReport(CrfReportMixin, BaseDeathReport):

    pass
