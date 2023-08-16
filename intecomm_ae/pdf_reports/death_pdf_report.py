from textwrap import fill

from edc_adverse_event.pdf_reports import DeathPdfReport as BaseDeathReport
from reportlab.lib.units import cm
from reportlab.platypus import Table


class DeathPdfReport(BaseDeathReport):
    weight_model = "intecomm_subject.followup"
    logo_data = {
        "app_label": "intecomm_edc",
        "filename": "meta_logo.png",
        "first_page": (4.0 * cm, 0.83 * cm),
        "later_pages": (3.0 * cm, 0.625 * cm),
    }

    def _draw_opinion(self, story):
        t = Table([["Section 2: Opinion of Local Study Doctor"]], (18 * cm))
        self.set_table_style(t, bg_cmd=self.bg_cmd)
        story.append(t)
        rows = []

        row = ["Main cause of death:"]
        if not self.death_report.cause_of_death:
            row.append(self.not_reported_text)
        else:
            row.append(fill(self.death_report.cause_of_death))
        rows.append(row)

        t = Table(rows, (4 * cm, 14 * cm))
        self.set_table_style(t, bg_cmd=self.bg_cmd)
        t.hAlign = "LEFT"
        story.append(t)

        self.draw_narrative(story, title="Narrative:", text=self.death_report.narrative)
