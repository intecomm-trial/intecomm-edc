from edc_constants.constants import DEAD, NONE, OTHER, UNKNOWN
from edc_ltfu.constants import LOST_TO_FOLLOWUP
from edc_transfer.constants import TRANSFERRED

from intecomm_prn.constants import LATE_EXCLUSION, OTHER_RX_DISCONTINUATION, WITHDRAWAL

list_data = {
    "intecomm_lists.offstudyreasons": [
        ("completed_followup", "Patient completed 36 months of follow-up"),
        ("clinical_withdrawal", "Patient is withdrawn on CLINICAL grounds ..."),
        ("clinical_endpoint", "Patient reached a clinical endpoint"),
        ("toxicity", "Patient experienced an unacceptable toxicity"),
        (
            "intercurrent_illness",
            "Intercurrent illness which prevents further treatment",
        ),
        (LOST_TO_FOLLOWUP, "Patient lost to follow-up"),
        (DEAD, "Patient reported/known to have died"),
        (WITHDRAWAL, "Patient withdrew consent to participate further"),
        (LATE_EXCLUSION, "Patient fulfilled late exclusion criteria*"),
        (TRANSFERRED, "Patient has been transferred to another health centre"),
        (
            OTHER_RX_DISCONTINUATION,
            "Other condition that justifies the discontinuation of "
            "treatment in the clinician’s opinion (specify below)",
        ),
        (
            OTHER,
            "Other reason (specify below)",
        ),
    ],
    "intecomm_lists.subjectvisitmissedreasons": [
        ("forgot", "Forgot / Can’t remember being told about appointment"),
        ("family_emergency", "Family emergency (e.g. funeral) and was away"),
        ("travelling", "Away travelling/visiting"),
        ("working_schooling", "Away working/schooling"),
        ("too_sick", "Too sick or weak to come to the centre"),
        ("lack_of_transport", "Transportation difficulty"),
        (OTHER, "Other reason (specify below)"),
    ],
}
