import pandas as pd
from edc_constants.constants import OTHER
from edc_pdutils.dataframes import get_crf
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM

mappings = {
    (
        "to get her medication now need fingerprints and physical "
        "presence of patient at hospital"
    ): "drug_refill",
    "needs fingerprints to access her drugs": "drug_refill",
    "drug pick up": "drug_refill",
    "he is using medication that are available through insurance": "drug_refill",
    "for drug refills": "drug_refill",
    "came for drug refills, completed eleventh month at the community": "drug_refill",
    "drug refills": "drug_refill",
    "patient visited for drug refills": "drug_refill",
    "patient reffer herself to hospital for specialist care": "self_referral",
    "patient visit for further management and collecting drugs": "self_referral",
    "for drug refill": "drug_refill",
    "come for drug reffil": "drug_refill",
    "she missed her refills at the community": "drug_refill",
    "patient came to seek care for the illness": "self_referral",
    "lack of sleep and difficult in breathing": "self_referral",
    "had an orthopedic clinic so she refilled drugs for htn and dm": "drug_refill",
    "patient attended to collect drugs": "drug_refill",
    "visited for drug refills": "drug_refill",
    "drug reffils for hiv": "drug_refill",
    "patient come for refills as she completed elevenths months at the comunity": (
        "drug_refill"
    ),
    "patient visit facility for further care because last seen patient got compication": (
        "referral"
    ),
    "patient was having nhif insurance has to attend favility for finger print": "drug_refill",
    "she has finished her  drugs": "drug_refill",
    "patient came for drug refill": "drug_refill",
    "patient was sick and so attended to the facility": "self_referral",
    "nhif patient attending facility": "drug_refill",
    "nhig patient attemdend facility": "drug_refill",
    "he is using medication that are available through insurance only": "drug_refill",
    "patient felt unwell and attended facility": "self_referral",
    "patient condition is not well to attend for community services": "self_referral",
    "the patient completed eleventh month at the community,come for drug refills": (
        "drug_refill"
    ),
    "patient wanted facility care because  of low payments for drugs": "drug_refill",
    (
        "missed visit came facilty for drug refil  and  "
        "did not meet a trial nurse came with details documented"
    ): "drug_refill",
    "patient was referred back to facility because she has early sign of foot ulcer": (
        "referral"
    ),
    (
        "missed her visit but also the foot ulce reoccur "
        "so she has to receive a treatment at hospital"
    ): "referral",
    (
        "patient got family emergency and want to travel, "
        "zasked to attend facility for drug refill"
    ): "drug_refill",
    "nseke": "unknown",
    "kalagala near market": "unknown",
    "mayembe gambogo": "unknown",
    "katende": "unknown",
    "katende trading center  near katende primary  school.": "unknown",
    "mpambire": "unknown",
    "moambire": "unknown",
    "kabila": "unknown",
    "kalagala": "unknown",
    "kibira": "unknown",
    "client completed elevenmonths at the community": "post_11_month_visit_at_facility",
    "patient completed eleventh months at the community": "post_11_month_visit_at_facility",
    "missed community appointment, attended at facility": "missed_community_appointment",
    "missed to attend community clinic, attended at facility": "missed_community_appointment",
    "she was sick during community clinic appointment.": "missed_community_appointment",
    (
        "patient got family emergency and want to travel, "
        "asked to attend facility for drug refill"
    ): "drug_refill",
}


def get_location_update(df_main: pd.DataFrame | None = None) -> pd.DataFrame:
    """Model LocationUpdate was required when appointment.appt_type
    (community or facility) conflicted with the randomization
    assignment (a=comm, b=facility).

    The CRF validates appt_type. Initially the CRF was always required
    and later only of values conflicted. You will see 'direction' as
    a->a, b->b -- in these cases the CRF did not need to be completed.

    You will also see a few b->a which is not possible. These are
    data entry errors.

    The case of interest is a->b.
    """

    def get_direction(s):
        if s.location == OTHER:
            return OTHER
        return f"{s.assignment}->{s.location}"

    def is_before_6m(s):
        if (s.report_datetime - s.baseline_datetime).days < 182:
            return 1
        return 0

    if not isinstance(df_main, pd.DataFrame):
        from .df_main_1858 import get_df_main_1858_pre

        df_main = get_df_main_1858_pre()

    # location update CRF was completed when appt_type did not match assignment
    df_location_update = get_crf(
        "intecomm_subject.locationupdate",
        subject_visit_model="intecomm_subject.subjectvisit",
        read_verbose=False,
    )
    # map location to assignment
    df_location_update["location"] = df_location_update["location"].map(
        {"community": COMMUNITY_ARM, "clinic": FACILITY_ARM, OTHER: OTHER}
    )
    # Was the subject expected to return to the community? Even
    # though often replied `NO`, the subject still returned. Can
    # ignore this column.
    df_location_update = df_location_update.rename(columns={"next_location": "returning"})

    # merge in vars from df_main
    df_location_update = df_location_update.merge(
        df_main[["subject_identifier", "assignment"]],
        how="left",
        on="subject_identifier",
    )
    # create new column 'direction' a->a, b->b or a->b
    df_location_update["direction"] = df_location_update.apply(get_direction, axis=1)
    # was the location update CRF submitted on or before 6m
    df_location_update["<182"] = df_location_update.apply(is_before_6m, axis=1)
    # get rid of "a->a", "b->b", "OTHER", CRF should not have been completed
    df_location_update = df_location_update[
        ~df_location_update.direction.isin(["a->a", "b->b", "OTHER"])
    ].copy()
    # baseline and endline visit are at facility regardless of assignment
    # remove them
    df_location_update = (
        df_location_update[
            (df_location_update.visit_code > 1000.0) & (df_location_update.visit_code < 1120.0)
        ]
        .copy()
        .sort_values(by=["subject_identifier", "visit_code"], ascending=[True, True])
        .reset_index(drop=True)
    )

    df_location_update = df_location_update.rename(columns={"comments": "location_comment"})
    df_location_update.loc[df_location_update.location_comment == "", "location_comment"] = (
        pd.NA
    )
    df_location_update["location_comment"] = df_location_update.location_comment.str.lower()
    df_location_update["location_comment"] = df_location_update.location_comment.replace(
        mappings
    )
    df_location_update = df_location_update.reset_index(drop=True)
    return df_location_update
