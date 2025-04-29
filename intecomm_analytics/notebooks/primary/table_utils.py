import pandas as pd
from edc_constants.constants import NO, YES
from great_tables import GT, html, loc, style
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM

from intecomm_analytics.constants import DM_ALONE, HIV_ALONE, HTN_ALONE, HTN_DM
from intecomm_analytics.dataframes import treatment_arm_labels as treatment_arm

__all__ = [
    "get_cells_for_continuous_var",
    "get_cells_for_yes_no",
    "get_formatted_rows_yes_no",
    "get_cells_for_yes_no_missing",
    "get_formatted_rows_by_country",
    "get_primary_cohorts_for_continuous_var",
    "get_primary_cohorts_cells_for_continuous_var",
]


def get_primary_cohorts_cells_for_continuous_var(
    df,
    col: str = None,
    arm: str = None,
    statistic: str = None,
) -> str | None:
    stat = None
    describe = df[df.assignment == arm][col].describe()
    if statistic == "count":
        stat = f"{int(describe['count'])}"
    elif statistic == "mean":
        stat = f"{describe['mean']:.2f}({describe['std']:.2f})"
    elif statistic == "median":
        stat = f"{describe['50%']:.2f}({describe['min']:.2f}–{describe['max']:.2f})"
    elif statistic == "median_iqr":
        stat = f"{describe['50%']:.2f}({describe['25%']:.2f}–{describe['75%']:.2f})"
    return stat


def get_primary_cohorts_for_continuous_var(df: pd.DataFrame, col: str, statistics: list[str]):
    """Returns 5 columns by primary cohorts of NCDS, HIV alone.

    Statistics, Comm NCD, Facility NCD, Comm HIV alone, Facility HIV alone.
    """
    cohorts = {"ncd": "Ncd", "hiv_only": "Hiv only"}
    statistics.insert(0, "count")
    rows = {}
    rows.update({"Statistics": statistics})
    for cohort_col, name in cohorts.items():
        for _arm in [COMMUNITY_ARM, FACILITY_ARM]:
            values = [
                get_primary_cohorts_cells_for_continuous_var(
                    df[getattr(df, cohort_col) == 1],
                    col,
                    arm=_arm,
                    statistic=statistic,
                )
                for statistic in statistics
            ]
            rows.update({f"{treatment_arm[_arm]} {name}": values})
    return rows


def get_primary_cohorts_by_categorical_column(df: pd.DataFrame, col: str):
    """Returns 5 columns by primary cohorts of NCDS, HIV alone.

    Statistics, Comm NCD, Facility NCD, Comm HIV alone, Facility HIV alone.
    """
    cohorts = {"ncd": "Ncd", "hiv_only": "Hiv only"}

    func = get_cells_for_categorical

    col_categories = df[df[col].notna()][col].unique().tolist()
    rows = {}
    rows.update({"Statistics": ["n", *col_categories]})
    for cohort_col, name in cohorts.items():
        for _arm in [COMMUNITY_ARM, FACILITY_ARM]:
            rows.update(
                {
                    f"{treatment_arm[_arm]} {name}": [
                        *func(
                            df[getattr(df, cohort_col) == 1],
                            col,
                            arm=_arm,
                            categories=col_categories,
                        )
                    ]
                }
            )
    return rows


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


def get_cells_for_categorical(
    df: pd.DataFrame, col: str, arm: str | None = None, categories: list | None = None
) -> list[str]:
    if arm:
        n = len(df[(df["assignment"] == arm) & (df[col].notna())])
        counts = df[(df["assignment"] == arm) & (df[col].notna())][col].value_counts(
            dropna=False
        )
        percentages = (
            df[(df["assignment"] == arm) & (df[col].notna())][col].value_counts(
                normalize=True, dropna=False
            )
            * 100
        )
    else:
        n = len(df[(df[col].notna())])
        counts = df[(df[col].notna())][col].value_counts(dropna=False)
        percentages = (
            df[(df[col].notna())][col].value_counts(normalize=True, dropna=False) * 100
        )

    cells = [
        f"{counts.get(category, 0)} ({percentages.get(category, 0):.1f}%)"
        for category in (categories or df[df[col].notna()][col].unique().tolist())
    ]
    return [n, *cells]


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


def get_formatted_rows_categorical_by_country(
    df: pd.DataFrame, col: str, mapping: dict | None = None
):
    """Returns 5 columns"""
    rows = {}
    if mapping:
        df = df.copy()
        df[col] = df[col].apply(lambda x: mapping[x] if pd.notna(x) else x)
    func = get_cells_for_categorical

    categories = df[df[col].notna()][col].unique().tolist()

    rows.update(
        {
            "Statistics": ["n", *categories],
        }
    )
    rows.update(
        {
            f"{treatment_arm[COMMUNITY_ARM]} UG": [
                *func(df[df.country == "UG"], col, arm="a"),
            ],
            f"{treatment_arm[COMMUNITY_ARM]} TZ": [
                *func(df[df.country == "TZ"], col, arm="a"),
            ],
            f"{treatment_arm[COMMUNITY_ARM]} BOTH": [
                *func(df, col, arm="a"),
            ],
            f"{treatment_arm[FACILITY_ARM]} UG": [
                *func(df[df.country == "UG"], col, arm="b"),
            ],
            f"{treatment_arm[FACILITY_ARM]} TZ": [
                *func(df[df.country == "TZ"], col, arm="b"),
            ],
            f"{treatment_arm[FACILITY_ARM]} BOTH": [
                *func(df, col, arm="b"),
            ],
            "All": [*func(df, col)],
        }
    )
    return rows


def get_formatted_rows_by_country(
    df,
    col_baseline: str | None = None,
    col_endline: str | None = None,
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


def get_great_table(df, group_row_headers, title: str, source_notes: str | None = None):
    tbl_groups = df.assign(group=group_row_headers)
    tbl_groups = tbl_groups[tbl_groups["group"] != ""]
    tbl_groups["Statistics"] = tbl_groups["Statistics"].apply(
        lambda x: f"&nbsp;&nbsp;&nbsp;{x}"
    )
    great_tbl = (
        GT(tbl_groups)
        .tab_header(title=title)
        .tab_spanner(
            label=html(
                "Participants with diabetes,<BR>hypertension, or both<br>"
                f"(n={df.loc[0, ['Community Ncd', 'Facility Ncd']].sum()})"
            ),
            columns=[1, 2],
        )
        .tab_spanner(
            label=html(
                "Participants with<BR>HIV alone<BR>"
                f"(n={df.loc[0, ['Community Hiv only', 'Facility Hiv only']].sum()})"
            ),
            columns=[3, 4],
        )
        .cols_label(
            {
                "Community Ncd": html(
                    f"Community<BR>(n={df.loc[0, ['Community Ncd']].sum()})"
                ),
                "Facility Ncd": html(f"Facility<br>(n={df.loc[0, ['Facility Ncd']].sum()})"),
                "Community Hiv only": html(
                    f"Community<br>(n={df.loc[0, ['Community Hiv only']].sum()})"
                ),
                "Facility Hiv only": html(
                    f"Facility<br>(n={df.loc[0, ['Facility Hiv only']].sum()})"
                ),
            }
        )
        .cols_align(align="left", columns=[0])
        .cols_align(align="center", columns=[1, 2, 3, 4])
        .tab_stub(rowname_col="Statistics", groupname_col="group")
        .opt_stylize(style=3)
        .opt_row_striping(row_striping=False)
        .opt_vertical_padding(scale=1.2)
        .opt_horizontal_padding(scale=1.0)
        .tab_options(
            stub_background_color="white",
            row_group_border_bottom_style="hidden",
            row_group_padding=0.5,
            row_group_background_color="white",
            table_background_color="white",
            table_font_size=12,
        )
        .tab_style(
            style=[style.fill(color="white"), style.text(color="black")],
            locations=loc.body(columns=[1, 2, 3, 4], rows=list(range(0, len(df)))),
        )
        .tab_source_note(source_note=html(source_notes or ""))
        .tab_style(
            style=style.text(color="black", size="small"),
            locations=loc.footer(),
        )
    )
    return great_tbl


def get_bp(df1, col, cond, label):
    col = col or "bp_controlled_endline"
    df1.loc[cond, col] = df1.loc[cond, col].fillna(-1)
    tbl_dct = get_primary_cohorts_by_categorical_column(df1[cond], col)
    dftbl = pd.DataFrame(tbl_dct)
    mapping = {"n": "n", -1: "Missing", 1: label, 0: "Uncontrolled"}
    dftbl["Statistics"] = dftbl["Statistics"].map(mapping)
    dftbl["Statistics"] = pd.Categorical(
        dftbl["Statistics"], categories=["n", label, "Uncontrolled", "Missing"], ordered=True
    )
    dftbl = dftbl.sort_values(by=["Statistics"], ascending=True)
    dftbl = dftbl.reset_index(drop=True)
    for col in ["Community Ncd", "Facility Ncd"]:
        value = dftbl.loc[1, col].split(" ")
        value = [value[0], "/", str(dftbl.loc[0, col]), " ", value[1]]
        value = "".join(value)
        dftbl.loc[1, col] = value
    dftbl.replace("0 (0.0%)", "NA", inplace=True)
    dftbl = dftbl.drop(0)
    dftbl = dftbl.reset_index(drop=True)
    return dftbl


def get_glucose(df1, col, cond, label):
    col = col or "glucose_controlled_endline"
    df1.loc[cond, col] = df1.loc[cond, col].fillna(-1)
    tbl_dct = get_primary_cohorts_by_categorical_column(df1[cond], col)
    dftbl = pd.DataFrame(tbl_dct)
    mapping = {"n": "n", -1: "Missing", 1: label, 0: "Uncontrolled"}
    dftbl["Statistics"] = dftbl["Statistics"].map(mapping)
    dftbl["Statistics"] = pd.Categorical(
        dftbl["Statistics"], categories=["n", label, "Uncontrolled", "Missing"], ordered=True
    )
    dftbl = dftbl.sort_values(by=["Statistics"], ascending=True)
    dftbl = dftbl.reset_index(drop=True)
    for col in ["Community Ncd", "Facility Ncd"]:
        value = dftbl.loc[1, col].split(" ")
        value = [value[0], "/", str(dftbl.loc[0, col]), " ", value[1]]
        value = "".join(value)
        dftbl.loc[1, col] = value
    dftbl.replace("0 (0.0%)", "NA", inplace=True)
    dftbl = dftbl.drop(0)
    dftbl = dftbl.reset_index(drop=True)
    return dftbl


def get_vl(df1, col, cond, label):
    col = col or "vl_controlled_endline"
    df1.loc[cond, "vl_controlled_endline"] = df1.loc[cond, "vl_controlled_endline"].fillna(-1)
    tbl_dct = get_primary_cohorts_by_categorical_column(df1[cond], "vl_controlled_endline")
    dftbl = pd.DataFrame(tbl_dct)
    mapping = {"n": "n", -1: "Missing", 1: label, 0: "Uncontrolled"}
    dftbl["Statistics"] = dftbl["Statistics"].map(mapping)
    dftbl["Statistics"] = pd.Categorical(
        dftbl["Statistics"], categories=["n", label, "Uncontrolled", "Missing"], ordered=True
    )
    dftbl = dftbl.sort_values(by=["Statistics"], ascending=True)
    dftbl = dftbl.reset_index(drop=True)
    for col in ["Community Hiv only", "Facility Hiv only"]:
        value = dftbl.loc[1, col].split(" ")
        value = [value[0], "/", str(dftbl.loc[0, col]), " ", value[1]]
        value = "".join(value)
        dftbl.loc[1, col] = value
    dftbl.replace("0 (0.0%)", "NA", inplace=True)
    dftbl = dftbl.drop(0)
    dftbl = dftbl.reset_index(drop=True)
    return dftbl


def _get_bin_labels_for_days_to_event(labels, bins):
    if not labels:
        labels = []
        for i in range(len(bins) - 1):
            if i == 0:
                labels.append(f"<{bins[i + 1] + 1}")
            elif i == len(bins) - 2:
                labels.append(f">={bins[i] + 1}")
            else:
                labels.append(f"{bins[i] + 1} to <{bins[i + 1] + 1}")
    return labels


def get_columns_for_days_to_event(
    df1: pd.DataFrame,
    col: str,
    bins: list[int] | None = None,
    labels: list[str] | None = None,
    set_zero_to_na: list[str] | None = None,
    drop_first: bool | None = None,
) -> pd.DataFrame:

    set_zero_to_na = set_zero_to_na or []
    bins = bins or [0, 181, 269, 364, 539, 1000]
    df1["days_to_event_bins"] = pd.cut(
        df1[col],
        bins,
        labels=_get_bin_labels_for_days_to_event(labels, bins),
    )
    tbl_dct = get_primary_cohorts_by_categorical_column(df1, "days_to_event_bins")
    dftbl = pd.DataFrame(tbl_dct)
    data = ["Median, (min-max)"]
    for primary_cohort in [[DM_ALONE, HTN_ALONE, HTN_DM], [HIV_ALONE]]:
        cohort_cond = getattr(df1, "primary_cohort").isin(primary_cohort)
        for arm in [COMMUNITY_ARM, FACILITY_ARM]:
            if df1[(df1.assignment == arm) & cohort_cond][col].isna().all():
                data.append("0 (0-0)")
            else:
                data.append(
                    f"{round(df1[(df1.assignment == arm) & cohort_cond][col].median(), 1)} "
                    f"({round(df1[(df1.assignment == arm) & cohort_cond][col].min(), 1)}-"
                    f"{round(df1[(df1.assignment == arm) & cohort_cond][col].max(), 1)})"
                )
    dftbl.loc[len(dftbl)] = data
    dftbl["Statistics"] = pd.Categorical(
        dftbl["Statistics"], categories=["n", "Median, range", *labels], ordered=True
    )
    dftbl = dftbl.sort_values(by=["Statistics"], ascending=True).replace(
        "0 (nan%)", "0 (0.0%)"
    )
    for cohort_label in set_zero_to_na:
        for column_name in dftbl.columns:
            if cohort_label in column_name.lower():
                dftbl[column_name] = dftbl[column_name].replace("0 (0.0%)", "NA")
                dftbl[column_name] = dftbl[column_name].replace("0 (0-0)", "NA")
    if drop_first:
        dftbl = dftbl.drop(0)
    dftbl = dftbl.reset_index(drop=True)
    return dftbl


def get_ineligible_reason(s):
    """Return a Series of reasons ineligible recoded.

    Many have multiple reasons, favor a primary reason like
    "pregnant", "not in care for 6m", etc
    """
    if pd.notna(s["reasons_ineligible"]):
        if s["reasons_ineligible"] in [
            "Does not live in catchment area",
            "Does not live in catchment area|Unable/Unwilling to stay in catchment area",
            (
                "Does not live in catchment area|Unable/Unwilling to stay in catchment area|"
                "Unsuitable for study|Unsuitable agreed by study coordinator"
            ),
            (
                "Does not live in catchment area|Unsuitable for study|"
                "Unsuitable agreed by study coordinator"
            ),
            "Unable/Unwilling to stay in catchment area",
            "Unable/Unwilling to stay in catchment area|Unsuitable for study",
        ]:
            return "Unable/Unwilling to stay in catchment area"
        elif s["reasons_ineligible"] in [
            "Unsuitable for study|Unsuitable agreed by study coordinator",
            "Unsuitable for study",
        ]:
            return "Unsuitable for study|Unsuitable agreed by study coordinator"
        elif s["reasons_ineligible"] in [
            "BP high",
            "BP history",
            "BP history|Glucose history",
            "BP history|Glucose history|Unsuitable for study",
            "BP history|Unable/Unwilling to stay in catchment area",
            "BP history|Unsuitable for study",
            "BP history|Unsuitable for study|Unsuitable agreed by study coordinator",
            "DM complication",
            "Glucose history",
            (
                "Glucose history|Glucose history|Unsuitable for study|"
                "Unsuitable agreed by study coordinator"
            ),
            (
                "Glucose history|Unable/Unwilling to stay in catchment area|"
                "Unsuitable for study|Unsuitable agreed by study coordinator"
            ),
            "Glucose history|Unsuitable for study",
            "Glucose history|Unsuitable for study|Unsuitable agreed by study coordinator",
            "HTN complication",
        ]:
            return "BP/glucose unstable history"
        elif s["reasons_ineligible"] in [
            "BP history|Requires acute care",
            "BP history|Requires acute care|Unsuitable for study",
            (
                "BP history|Requires acute care|Unsuitable for study|"
                "Unsuitable agreed by study coordinator"
            ),
            "Glucose history|Requires acute care",
            (
                "Glucose history|Requires acute care|"
                "Unsuitable for study|Unsuitable agreed by study coordinator"
            ),
            "Requires acute care|Unable/Unwilling to stay in catchment area",
            "Requires acute care|Unsuitable for study",
            "Requires acute care|Unsuitable for study|Unsuitable agreed by study coordinator",
        ]:
            return "Requires acute care"
        elif s["reasons_ineligible"] in [
            "BP history|Glucose history|Pregnant|Requires acute care",
            (
                "Does not live in catchment area|Pregnant|"
                "Unable/Unwilling to stay in catchment area"
            ),
            "Pregnant|Requires acute care|Unsuitable for study",
            "Pregnant|Unsuitable for study",
            "Pregnant|Unsuitable for study|Unsuitable agreed by study coordinator",
        ]:
            return "Pregnant"
        elif s["reasons_ineligible"] in [
            "BP history|Not in care for 6m",
            "Glucose history|Not in care for 6m",
            (
                "Not in care for 6m|Does not live in catchment area|"
                "Unable/Unwilling to stay in catchment area"
            ),
        ]:
            return "Not in care for 6m"
        else:
            return s["reasons_ineligible"]
    return s["reasons_ineligible"]
