from edc_lab_panel.constants import FBC, LFT, LIPIDS, RFT
from edc_lab_panel.panels import fbc_panel, lft_panel, lipids_panel, rft_panel
from edc_qareports.sql_generator import CrfCase, RequisitionCase

qa_cases = [
    RequisitionCase(
        label="FBC requisitioned but not entered",
        dbtable="intecomm_subject_bloodresultsfbc",
        label_lower="intecomm_subject.bloodresultsfbc",
        panel=FBC,
    ),
    RequisitionCase(
        label="RFT requisitioned but not entered",
        dbtable="intecomm_subject_bloodresultsrft",
        label_lower="intecomm_subject.bloodresultsrft",
        panel=RFT,
    ),
    RequisitionCase(
        label="LFT requisitioned but not entered",
        dbtable="intecomm_subject_bloodresultslft",
        label_lower="intecomm_subject.bloodresultslft",
        panel=LFT,
    ),
    RequisitionCase(
        label="LIPIDS requisitioned but not entered",
        dbtable="intecomm_subject_bloodresultslipids",
        label_lower="intecomm_subject.bloodresultslipids",
        panel=LIPIDS,
    ),
]

panels = {FBC: fbc_panel, RFT: rft_panel, LFT: lft_panel, LIPIDS: lipids_panel}
for abbrev, panel in panels.items():
    for utest_id in panel.utest_ids:
        try:
            utest_id, _ = utest_id
        except ValueError:
            pass
        qa_cases.append(
            CrfCase(
                label=f"{abbrev.upper()}: missing {utest_id} value/units",
                dbtable=f"intecomm_subject_bloodresults{abbrev.lower()}",
                label_lower=f"intecomm_subject.bloodresults{abbrev.lower()}",
                where=f"crf.{utest_id}_value is null or crf.{utest_id}_units is null",
            )
        )

    CrfCase(
        label="No UREA value",
        dbtable="intecomm_subject_bloodresultsrft",
        label_lower="intecomm_subject.bloodresultsrft",
        where="crf.urea_value is null or crf.urea_units is null",
    ),
