import pandas as pd
from edc_analytics import RowDefinition
from edc_analytics.constants import N_ONLY, N_WITH_ROW_PROP
from edc_analytics.custom_tables import AgeTable
from edc_analytics.row import RowDefinitions
from edc_analytics.table import Table
from edc_constants.constants import FEMALE, MALE


class TableOne(Table):

    def __init__(self, main_df: pd.DataFrame = None):
        super().__init__(colname="", main_df=main_df)

    @property
    def row_definitions(self) -> RowDefinitions:
        row_defs = super().row_definitions
        row_defs.add(
            RowDefinition(
                title="Uganda",
                label=self.default_sublabel,
                colname=None,
                condition=(
                    (self.main_df.site_id < 200) & (self.main_df[self.gender_column].notna())
                ),
                columns={
                    FEMALE: (N_WITH_ROW_PROP, 2),
                    MALE: (N_WITH_ROW_PROP, 2),
                    "All": (N_ONLY, 2),
                },
                drop=False,
            )
        )
        row_defs.add(
            RowDefinition(
                title="Tanzania",
                label=self.default_sublabel,
                colname=None,
                condition=(
                    (self.main_df.site_id >= 200) & (self.main_df[self.gender_column].notna())
                ),
                columns={
                    FEMALE: (N_WITH_ROW_PROP, 2),
                    MALE: (N_WITH_ROW_PROP, 2),
                    "All": (N_ONLY, 2),
                },
                drop=False,
            )
        )
        row_defs.extend(AgeTable(main_df=self.main_df).row_definitions)

        return row_defs
