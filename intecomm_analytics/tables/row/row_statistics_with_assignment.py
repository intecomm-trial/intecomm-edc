import pandas as pd
from edc_analytics import RowStatistics
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM


class RowStatisticsCommunity(RowStatistics):
    def __init__(
        self,
        df_numerator: pd.DataFrame = None,
        df_denominator: pd.DataFrame = None,
        **kwargs,
    ):
        df_numerator = df_numerator.loc[df_numerator["assignment"] == COMMUNITY_ARM]
        super().__init__(
            df_numerator=df_numerator,
            df_denominator=df_denominator,
            **kwargs,
        )


class RowStatisticsFacility(RowStatistics):
    def __init__(
        self,
        df_numerator: pd.DataFrame = None,
        df_denominator: pd.DataFrame = None,
        **kwargs,
    ):
        df_numerator = df_numerator.loc[df_numerator["assignment"] == FACILITY_ARM]
        super().__init__(
            df_numerator=df_numerator,
            df_denominator=df_denominator,
            **kwargs,
        )


class RowStatisticsWithAssignment(RowStatistics):
    def __init__(
        self,
        columns: dict[str, tuple[str, int]] = None,
        df_all: pd.DataFrame = None,
        coltotal: float | int | None = None,
        **kwargs,
    ):
        """
        custom row for displaying with gender columns: F, M, All
        :param colname:
        :param df_numerator:
        :param df_denominator:
        :param df_all:
        :param columns: dict of {col: (style name, places)} where col
               is "F", "M" or "All"

        Note: the default df["gender"] is "M" or "F".
        """

        community_style, community_places = columns[COMMUNITY_ARM]
        facility_style, facility_places = columns[FACILITY_ARM]
        all_style, all_places = columns["All"]

        super().__init__(
            places=all_places,
            style=all_style,
            df_all=df_all,
            coltotal=coltotal,
            **kwargs,
        )

        self.community = RowStatisticsCommunity(
            places=community_places,
            style=community_style,
            coltotal=len(df_all[df_all["assignment"] == COMMUNITY_ARM]),
            df_all=df_all,
            **kwargs,
        )
        self.facility = RowStatisticsFacility(
            places=facility_places,
            style=facility_style,
            coltotal=len(df_all[df_all["assignment"] == FACILITY_ARM]),
            df_all=df_all,
            **kwargs,
        )

    def values_list(self, style: str | None = None, places: int | None = None) -> list:
        values_list = super().values_list()
        return (
            list(self.formatted_cells().values())
            + self.community.values_list()
            + self.facility.values_list()
            + values_list
        )

    def labels(self) -> list[str]:
        labels = super().labels()
        return (
            list(self.formatted_cells().keys())
            + [f"a{x}" for x in self.community.labels()]
            + [f"b{x}" for x in self.facility.labels()]
            + labels
        )

    def row(self):
        return [self.formatted_cells()] + self.values_list()

    def formatted_cells(self) -> dict:
        formatted_cell = super().formatted_cell()
        return dict(
            A=self.community.formatted_cell(),
            B=self.facility.formatted_cell(),
            All=formatted_cell,
        )
