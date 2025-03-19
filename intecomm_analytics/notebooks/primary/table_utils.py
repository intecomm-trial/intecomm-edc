import pandas as pd
from edc_constants.constants import NO, YES
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM

from intecomm_analytics.dataframes import treatment_arm_labels as treatment_arm

__all__ = [
    "get_cells_for_continuous_var",
    "get_cells_for_yes_no",
    "get_formatted_rows_yes_no",
    "get_cells_for_yes_no_missing",
    "get_formatted_rows_by_country",
]


def get_cells_for_continuous_var(df) -> list[str]:
    return [
        f"{int(df['count'])}",
        f"{df['mean']:.2f}({df['std']:.2f})",
        f"{df['50%']:.2f}({df['min']:.2f}–{df['max']:.2f})",
    ]


def get_cells_for_yes_no(df: pd.DataFrame, col: str, arm: str | None = None) -> list[str]:
    if arm:
        n = len(df[(df["assignment"] == arm) & (df[col].notna())])
        counts = df[(df["assignment"] == arm) & (df[col].notna())][col].value_counts()
        percentages = (
            df[(df["assignment"] == arm) & (df[col].notna())][col].value_counts(normalize=True)
            * 100
        )
    else:
        n = len(df[(df[col].notna())])
        counts = df[(df[col].notna())][col].value_counts()
        percentages = df[(df[col].notna())][col].value_counts(normalize=True) * 100
    return [
        n,
        f"{counts.get(YES, 0)} ({percentages.get(YES, 0):.1f}%)",
        f"{counts.get(NO, 0)} ({percentages.get(NO, 0):.1f}%)",
    ]


def get_cells_for_yes_no_missing(
    df: pd.DataFrame, col: str, arm: str | None = None
) -> list[str]:
    if arm:
        n = len(df[(df["assignment"] == arm) & (df[col].notna())])
        counts = df[(df["assignment"] == arm) & (df[col].notna())][col].value_counts()
        percentages = (
            df[(df["assignment"] == arm) & (df[col].notna())][col].value_counts(normalize=True)
            * 100
        )
    else:
        n = len(df[(df[col].notna())])
        counts = df[(df[col].notna())][col].value_counts()
        percentages = df[(df[col].notna())][col].value_counts(normalize=True) * 100
    return [
        n,
        f"{counts.get(YES, 0)} ({percentages.get(YES, 0):.1f}%)",
        f"{counts.get(NO, 0)} ({percentages.get(NO, 0):.1f}%)",
        f"{counts.get('Missing', 0)} ({percentages.get('Missing', 0):.1f}%)",
    ]


def get_formatted_rows_yes_no(
    df_base: pd.DataFrame,
    df_end: pd.DataFrame,
    baseline_col: str,
    endline_col: str,
    missing: bool | None = None,
):
    """Returns 5 columns"""
    rows = {}
    if missing:
        func = get_cells_for_yes_no_missing
        rows.update(
            {
                "Timepoint": ["Baseline", "", "", "", "Endline", "", "", ""],
                "Statistics": ["n", "Yes", "No", "Missing", "n", "Yes", "No", "Missing"],
            }
        )
    else:
        func = get_cells_for_yes_no
        rows.update(
            {
                "Timepoint": ["Baseline", "", "", "Endline", "", ""],
                "Statistics": [
                    "n",
                    "Yes",
                    "No",
                    "n",
                    "Yes",
                    "No",
                ],
            }
        )
    rows.update(
        {
            f"{treatment_arm[COMMUNITY_ARM]} UG": [
                *func(df_base[df_base.country == "UG"], baseline_col, arm="a"),
                *func(df_end[df_end.country == "UG"], endline_col, arm="a"),
            ],
            f"{treatment_arm[COMMUNITY_ARM]} TZ": [
                *func(df_base[df_base.country == "TZ"], baseline_col, arm="a"),
                *func(df_end[df_end.country == "TZ"], endline_col, arm="a"),
            ],
            f"{treatment_arm[COMMUNITY_ARM]} BOTH": [
                *func(df_base, baseline_col, arm="a"),
                *func(df_end, endline_col, arm="a"),
            ],
            f"{treatment_arm[FACILITY_ARM]} UG": [
                *func(df_base[df_base.country == "UG"], baseline_col, arm="b"),
                *func(df_end[df_end.country == "UG"], endline_col, arm="b"),
            ],
            f"{treatment_arm[FACILITY_ARM]} TZ": [
                *func(df_base[df_base.country == "TZ"], baseline_col, arm="b"),
                *func(df_end[df_end.country == "TZ"], endline_col, arm="b"),
            ],
            f"{treatment_arm[FACILITY_ARM]} BOTH": [
                *func(df_base, baseline_col, arm="b"),
                *func(df_end, endline_col, arm="b"),
            ],
            "All": [
                *func(df_base, baseline_col),
                *func(df_end, endline_col),
            ],
        }
    )
    return rows


def get_formatted_rows_by_country(
    df, col_baseline: str | None = None, col_endline: str | None = None
):
    """Returns 5 columns
    Baseline and endline format
    """

    df_base = df.copy()
    df_ug_base = df[(df.country == "UG")].copy()
    df_tz_base = df[(df.country == "TZ")].copy()

    baseline_ug_a = df_ug_base[(df_ug_base["assignment"] == COMMUNITY_ARM)][
        col_baseline
    ].describe()
    baseline_tz_a = df_tz_base[(df_tz_base["assignment"] == COMMUNITY_ARM)][
        col_baseline
    ].describe()
    baseline_a = df_base[df_base["assignment"] == COMMUNITY_ARM][col_baseline].describe()

    baseline_ug_b = df_ug_base[(df_ug_base["assignment"] == FACILITY_ARM)][
        col_baseline
    ].describe()
    baseline_tz_b = df_tz_base[(df_tz_base["assignment"] == FACILITY_ARM)][
        col_baseline
    ].describe()
    baseline_b = df_base[df_base["assignment"] == FACILITY_ARM][col_baseline].describe()

    baseline_all = df_base[col_baseline].describe()

    df_ug_end = df[(df.country == "UG") & (df["onstudy_days"] >= 182)].copy()
    df_tz_end = df[(df.country == "TZ") & (df["onstudy_days"] >= 182)].copy()
    df_end = df[(df["onstudy_days"] >= 182)].copy()

    endline_ug_a = df_ug_end[df_ug_end["assignment"] == COMMUNITY_ARM][col_endline].describe()
    endline_tz_a = df_tz_end[df_tz_end["assignment"] == COMMUNITY_ARM][col_endline].describe()
    endline_a = df_end[df_end["assignment"] == COMMUNITY_ARM][col_endline].describe()

    endline_ug_b = df_ug_end[df_ug_end["assignment"] == FACILITY_ARM][col_endline].describe()
    endline_tz_b = df_tz_end[df_tz_end["assignment"] == FACILITY_ARM][col_endline].describe()
    endline_b = df_end[df_end["assignment"] == FACILITY_ARM][col_endline].describe()

    endline_all = df_end[col_endline].describe()

    return {
        "Timepoint": ["Baseline", "", "", "Endline", "", ""],
        "Statistics": ["n", "Mean(sd)", "Median(min-max)", "n", "Mean(sd)", "Median(min-max)"],
        f"{treatment_arm[COMMUNITY_ARM]} UG": [
            *get_cells_for_continuous_var(baseline_ug_a),
            *get_cells_for_continuous_var(endline_ug_a),
        ],
        f"{treatment_arm[COMMUNITY_ARM]} TZ": [
            *get_cells_for_continuous_var(baseline_tz_a),
            *get_cells_for_continuous_var(endline_tz_a),
        ],
        f"{treatment_arm[COMMUNITY_ARM]} BOTH": [
            *get_cells_for_continuous_var(baseline_a),
            *get_cells_for_continuous_var(endline_a),
        ],
        f"{treatment_arm[FACILITY_ARM]} UG": [
            *get_cells_for_continuous_var(baseline_ug_b),
            *get_cells_for_continuous_var(endline_ug_b),
        ],
        f"{treatment_arm[FACILITY_ARM]} TZ": [
            *get_cells_for_continuous_var(baseline_tz_b),
            *get_cells_for_continuous_var(endline_tz_b),
        ],
        f"{treatment_arm[FACILITY_ARM]} BOTH": [
            *get_cells_for_continuous_var(baseline_b),
            *get_cells_for_continuous_var(endline_b),
        ],
        "All": [
            *get_cells_for_continuous_var(baseline_all),
            *get_cells_for_continuous_var(endline_all),
        ],
    }


def get_formatted_rows_by_country_single(
    df, col_baseline: str | None = None, col_endline: str | None = None
):
    """Returns 5 columns"""

    df_base = df.copy()
    df_ug_base = df[(df.country == "UG")].copy()
    df_tz_base = df[(df.country == "TZ")].copy()

    baseline_ug_a = df_ug_base[(df_ug_base["assignment"] == COMMUNITY_ARM)][
        col_baseline
    ].describe()
    baseline_tz_a = df_tz_base[(df_tz_base["assignment"] == COMMUNITY_ARM)][
        col_baseline
    ].describe()
    baseline_a = df_base[df_base["assignment"] == COMMUNITY_ARM][col_baseline].describe()

    baseline_ug_b = df_ug_base[(df_ug_base["assignment"] == FACILITY_ARM)][
        col_baseline
    ].describe()
    baseline_tz_b = df_tz_base[(df_tz_base["assignment"] == FACILITY_ARM)][
        col_baseline
    ].describe()
    baseline_b = df_base[df_base["assignment"] == FACILITY_ARM][col_baseline].describe()

    baseline_all = df_base[col_baseline].describe()

    return {
        "Timepoint": ["Baseline", "", ""],
        "Statistics": ["n", "Mean(sd)", "Median(min-max)"],
        f"{treatment_arm[COMMUNITY_ARM]} UG": [
            *get_cells_for_continuous_var(baseline_ug_a),
        ],
        f"{treatment_arm[COMMUNITY_ARM]} TZ": [
            *get_cells_for_continuous_var(baseline_tz_a),
        ],
        f"{treatment_arm[COMMUNITY_ARM]} BOTH": [
            *get_cells_for_continuous_var(baseline_a),
        ],
        f"{treatment_arm[FACILITY_ARM]} UG": [
            *get_cells_for_continuous_var(baseline_ug_b),
        ],
        f"{treatment_arm[FACILITY_ARM]} TZ": [
            *get_cells_for_continuous_var(baseline_tz_b),
        ],
        f"{treatment_arm[FACILITY_ARM]} BOTH": [
            *get_cells_for_continuous_var(baseline_b),
        ],
        "All": [
            *get_cells_for_continuous_var(baseline_all),
        ],
    }


# def get_formatted_rows_tstat(dfa, dfb, col: str | None = None):
#
#     t_stat, p_value = ttest_ind(dfa[col], dfb[col])
#
#     df_base = df.copy()
#     df_ug_base = df[(df.country == "UG")].copy()
#     df_tz_base = df[(df.country == "TZ")].copy()
#
#     baseline_ug_a = df_ug_base[(df_ug_base["assignment"] == COMMUNITY_ARM)][
#         col_baseline
#     ].describe()
#     baseline_tz_a = df_tz_base[(df_tz_base["assignment"] == COMMUNITY_ARM)][
#         col_baseline
#     ].describe()
#     baseline_a = df_base[df_base["assignment"] == COMMUNITY_ARM][col_baseline].describe()
#
#     baseline_ug_b = df_ug_base[(df_ug_base["assignment"] == FACILITY_ARM)][
#         col_baseline
#     ].describe()
#     baseline_tz_b = df_tz_base[(df_tz_base["assignment"] == FACILITY_ARM)][
#         col_baseline
#     ].describe()
#     baseline_b = df_base[df_base["assignment"] == FACILITY_ARM][col_baseline].describe()
#
#     baseline_all = df_base[col_baseline].describe()
#
#     return {
#         "Timepoint": ["Baseline", "", ""],
#         "Statistics": ["n", "Mean(sd)", "Median(min-max)"],
#         f"{treatment_arm[COMMUNITY_ARM]} UG": [
#             *get_cells_for_continuous_var(baseline_ug_a),
#         ],
#         f"{treatment_arm[COMMUNITY_ARM]} TZ": [
#             *get_cells_for_continuous_var(baseline_tz_a),
#         ],
#         f"{treatment_arm[COMMUNITY_ARM]} BOTH": [
#             *get_cells_for_continuous_var(baseline_a),
#         ],
#         f"{treatment_arm[FACILITY_ARM]} UG": [
#             *get_cells_for_continuous_var(baseline_ug_b),
#         ],
#         f"{treatment_arm[FACILITY_ARM]} TZ": [
#             *get_cells_for_continuous_var(baseline_tz_b),
#         ],
#         f"{treatment_arm[FACILITY_ARM]} BOTH": [
#             *get_cells_for_continuous_var(baseline_b),
#         ],
#         "All": [
#             *get_cells_for_continuous_var(baseline_all),
#         ],
#     }
