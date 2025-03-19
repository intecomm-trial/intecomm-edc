import pandas as pd
from edc_analytics import RowDefinition
from edc_analytics.constants import MEDIAN_IQR, N_ONLY, N_WITH_COL_PROP, N_WITH_ROW_PROP
from edc_analytics.custom_tables import AgeTable as BaseAgeTable
from edc_analytics.row import RowDefinitions
from edc_analytics.table import Table
from edc_constants.constants import FEMALE, MALE
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM

from .row import RowStatisticsWithAssignment


class AgeTable(BaseAgeTable):
    col_a = COMMUNITY_ARM
    col_b = FACILITY_ARM
    column_name = "assignment"
    row_statistics_cls = RowStatisticsWithAssignment


class TableTwo(Table):
    row_statistics_cls = RowStatisticsWithAssignment
    column = "assignment"

    def __init__(self, main_df: pd.DataFrame = None):
        super().__init__(colname="", main_df=main_df)

    @property
    def row_definitions(self) -> RowDefinitions:
        # row_defs = super().row_definitions
        row_defs = RowDefinitions()
        row_defs = self.add_assignment_row_defs(row_defs)
        row_defs = self.add_gender_row_defs(row_defs)
        row_defs.extend(AgeTable(main_df=self.main_df).row_definitions)
        row_defs = self.add_condition_row_defs(row_defs)
        row_defs = self.add_in_care_row_defs(row_defs)
        return row_defs

    def add_assignment_row_defs(self, row_defs) -> RowDefinitions:
        row_defs.add(
            RowDefinition(
                title="Country",
                label=self.default_sublabel,
                colname=None,
                condition=(self.main_df.assignment.notna()),
                columns={
                    COMMUNITY_ARM: (N_WITH_ROW_PROP, 2),
                    FACILITY_ARM: (N_WITH_ROW_PROP, 2),
                    "All": (N_ONLY, 2),
                },
                drop=False,
            )
        )
        row_defs.add(
            RowDefinition(
                title="",
                label="Uganda",
                colname=None,
                condition=(self.main_df.site_id < 200),
                columns={
                    COMMUNITY_ARM: (N_WITH_COL_PROP, 2),
                    FACILITY_ARM: (N_WITH_COL_PROP, 2),
                    "All": (N_ONLY, 2),
                },
                drop=False,
            )
        )
        row_defs.add(
            RowDefinition(
                title="",
                label="Tanzania",
                colname=None,
                condition=(self.main_df.site_id >= 200),
                columns={
                    COMMUNITY_ARM: (N_WITH_COL_PROP, 2),
                    FACILITY_ARM: (N_WITH_COL_PROP, 2),
                    "All": (N_ONLY, 2),
                },
                drop=False,
            )
        )
        return row_defs

    def add_gender_row_defs(self, row_defs) -> RowDefinitions:
        row_defs.add(
            RowDefinition(
                title="Gender",
                label=self.default_sublabel,
                colname=None,
                condition=(self.main_df.gender.notna()),
                columns={
                    COMMUNITY_ARM: (N_WITH_ROW_PROP, 2),
                    FACILITY_ARM: (N_WITH_ROW_PROP, 2),
                    "All": (N_ONLY, 2),
                },
                drop=False,
            )
        )
        row_defs.add(
            RowDefinition(
                title="",
                label="Female",
                colname=None,
                condition=(self.main_df.gender == FEMALE),
                columns={
                    COMMUNITY_ARM: (N_WITH_COL_PROP, 2),
                    FACILITY_ARM: (N_WITH_COL_PROP, 2),
                    "All": (N_ONLY, 2),
                },
                drop=False,
            )
        )
        row_defs.add(
            RowDefinition(
                title="",
                label="Male",
                colname=None,
                condition=(self.main_df.gender == MALE),
                columns={
                    COMMUNITY_ARM: (N_WITH_COL_PROP, 2),
                    FACILITY_ARM: (N_WITH_COL_PROP, 2),
                    "All": (N_ONLY, 2),
                },
                drop=False,
            )
        )
        return row_defs

    def add_condition_row_defs(self, row_defs) -> RowDefinitions:
        row_defs.add(
            RowDefinition(
                title="Conditions",
                label=self.default_sublabel,
                colname=None,
                condition=(self.main_df.assignment.notna()),
                columns={
                    COMMUNITY_ARM: (N_WITH_ROW_PROP, 2),
                    FACILITY_ARM: (N_WITH_ROW_PROP, 2),
                    "All": (N_ONLY, 2),
                },
                drop=False,
            )
        )
        row_defs.add(
            RowDefinition(
                title="",
                label="HIV",
                colname=None,
                condition=(self.main_df.hiv_only == 1),
                columns={
                    COMMUNITY_ARM: (N_WITH_COL_PROP, 2),
                    FACILITY_ARM: (N_WITH_COL_PROP, 2),
                    "All": (N_ONLY, 2),
                },
                drop=False,
            )
        )
        row_defs.add(
            RowDefinition(
                title="",
                label="NCD",
                colname=None,
                condition=(self.main_df.ncd == 1),
                columns={
                    COMMUNITY_ARM: (N_WITH_COL_PROP, 2),
                    FACILITY_ARM: (N_WITH_COL_PROP, 2),
                    "All": (N_ONLY, 2),
                },
                drop=False,
            )
        )
        row_defs.add(
            RowDefinition(
                title="",
                label="HIV+NCD",
                colname=None,
                condition=((self.main_df.hiv_only == 0) & (self.main_df.hiv == 1)),
                columns={
                    COMMUNITY_ARM: (N_WITH_COL_PROP, 2),
                    FACILITY_ARM: (N_WITH_COL_PROP, 2),
                    "All": (N_ONLY, 2),
                },
                drop=False,
            )
        )
        return row_defs

    def add_in_care_row_defs(self, row_defs) -> RowDefinitions:
        row_defs.add(
            RowDefinition(
                title="Years in care",
                label=self.default_sublabel,
                colname=None,
                condition=(self.main_df.assignment.notna()),
                columns={
                    COMMUNITY_ARM: (N_WITH_ROW_PROP, 2),
                    FACILITY_ARM: (N_WITH_ROW_PROP, 2),
                    "All": (N_ONLY, 2),
                },
                drop=False,
            )
        )
        row_defs.add(
            RowDefinition(
                title="",
                label="HIV only",
                colname="hiv_years_since_dx",
                condition=(self.main_df.hiv_only == 1),
                columns={
                    COMMUNITY_ARM: (MEDIAN_IQR, 2),
                    FACILITY_ARM: (MEDIAN_IQR, 2),
                    "All": (MEDIAN_IQR, 2),
                },
                drop=False,
            )
        )
        row_defs.add(
            RowDefinition(
                title="",
                label="HTN",
                colname="htn_years_since_dx",
                condition=(self.main_df.htn == 1),
                columns={
                    COMMUNITY_ARM: (MEDIAN_IQR, 2),
                    FACILITY_ARM: (MEDIAN_IQR, 2),
                    "All": (MEDIAN_IQR, 2),
                },
                drop=False,
            )
        )
        row_defs.add(
            RowDefinition(
                title="",
                label="DM",
                colname="dm_years_since_dx",
                condition=(self.main_df.dm == 1),
                columns={
                    COMMUNITY_ARM: (MEDIAN_IQR, 2),
                    FACILITY_ARM: (MEDIAN_IQR, 2),
                    "All": (MEDIAN_IQR, 2),
                },
                drop=False,
            )
        )
        return row_defs
