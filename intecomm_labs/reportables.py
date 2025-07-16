from edc_reportable.data import africa, daids_july_2017

grading_data = {}
grading_data.update(**daids_july_2017.dummies)
grading_data.update(**daids_july_2017.chemistries)
grading_data.update(**daids_july_2017.hematology)

collection_name = "intecomm"
normal_data = africa.normal_data
reportable_grades = [3, 4]
reportable_grades_exceptions = {}
