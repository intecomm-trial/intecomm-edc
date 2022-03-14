from edc_lab_panel.panels import (
    blood_glucose_panel,
    fbc_panel,
    hba1c_panel,
    insulin_panel,
    lft_panel,
    lipids_panel,
    rft_panel,
)
from edc_visit_schedule import FormsCollection, Requisition

requisitions_prn = FormsCollection(
    Requisition(show_order=200, panel=blood_glucose_panel, required=True, additional=False),
    Requisition(show_order=220, panel=hba1c_panel, required=True, additional=False),
    Requisition(show_order=230, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=240, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=250, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=260, panel=lipids_panel, required=True, additional=False),
    Requisition(show_order=270, panel=insulin_panel, required=True, additional=False),
    name="requisitions_prn",
)

requisitions_unscheduled = FormsCollection(
    Requisition(show_order=200, panel=blood_glucose_panel, required=True, additional=False),
    name="requisitions_unscheduled",
)

requisitions_d1 = FormsCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=40, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=60, panel=insulin_panel, required=True, additional=False),
    name="requisitions_day1",
)
