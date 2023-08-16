from textwrap import fill

from edc_adverse_event.pdf_reports import AePdfReport as BaseAeReport
from reportlab.lib.units import cm
from reportlab.platypus import Table


class AePdfReport(BaseAeReport):
    weight_model = "intecomm_subject.followup"
    logo_data = {
        "app_label": "intecomm_edc",
        "filename": "meta_logo.png",
        "first_page": (4.0 * cm, 0.83 * cm),
        "later_pages": (3.0 * cm, 0.625 * cm),
    }

    def _draw_ae_overview(self, story):
        # basics
        classification_text = fill(self.ae_initial.ae_classification_as_text, width=80)
        rows = [
            ["Reference:", self.ae_initial.identifier],
            [
                "Report date:",
                self.ae_initial.report_datetime.strftime("%Y-%m-%d %H:%M"),
            ],
            ["Awareness date:", self.ae_initial.ae_awareness_date.strftime("%Y-%m-%d")],
            ["Actual start date:", self.ae_initial.ae_start_date.strftime("%Y-%m-%d")],
            ["Classification:", classification_text],
            ["Severity:", self.ae_initial.get_ae_grade_display()],
        ]

        t = Table(rows, (4 * cm, 14 * cm))
        self.set_table_style(t, bg_cmd=self.bg_cmd)
        t.hAlign = "LEFT"
        story.append(t)

    def _draw_ae_drug_relationship(self, story):
        pass

    def _draw_ae_cause(self, story):
        pass
