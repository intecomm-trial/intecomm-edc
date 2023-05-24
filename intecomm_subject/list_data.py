from edc_constants.constants import DONT_KNOW, NONE, OTHER

list_data = {
    "edc_he.insurancetypes": [
        ("private", "Private/work-place/voluntary health insurance"),
        ("nhif", "NHIF (National Health Insurance Fund)"),
        ("chf", "CHF (Community Health Insurance Fund)"),
        ("club", "Patient support group / club"),
        (NONE, "None"),
        (DONT_KNOW, "Don’t know"),
        (OTHER, "Other, specify"),
    ],
    "edc_he.nationalities": [
        ("tanzania", "Tanzanian"),
        ("uganda", "Ugandan"),
        (NONE, "None of the above"),
    ],
    "edc_he.religions": [
        ("muslim", "Muslim"),
        ("seventh-day-adventist", "Seventh day Adventist"),
        ("assemblies-of-god", "Tanzanian Assemblies of God"),
        ("catholic", "Catholic"),
        ("lutheran", "Lutheran"),
        ("moravian", "Moravian"),
        ("pentecostal", "Pentecostal"),
        ("african-inland-church", "African Inland Church"),
        (NONE, "No religion"),
        (OTHER, "Other, specify"),
    ],
    "edc_he.ethnicities": [
        ("msukuma", "Msukuma"),
        ("mjita", "Mjita"),
        ("mzinza", "Mzinza"),
        ("myiramba", "Myiramba"),
        ("mkara-mkerewe", "Mkara/Mkerewe"),
        ("mhaya", "Mhaya"),
        ("mjaluo", "Mjaluo"),
        ("mkuria-mshashi", "Mkuria/Mshashi"),
        ("mchaga", "Mchaga"),
        ("mhindi", "Mhindi"),
        ("mwarabu", "Mwarabu"),
        (OTHER, "Other, specify"),
    ],
}
