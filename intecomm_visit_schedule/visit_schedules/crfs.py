from edc_visit_schedule import Crf, FormsCollection

# TODO: whats the difference between bloodresultsglu and glucose??

crfs_prn = FormsCollection(
    Crf(show_order=10, model="intecomm_subject.bloodresultsfbc"),
    Crf(show_order=150, model="intecomm_subject.glucose"),
    Crf(show_order=220, model="intecomm_subject.bloodresultsglu"),
    Crf(show_order=230, model="intecomm_subject.bloodresultshba1c"),
    Crf(show_order=240, model="intecomm_subject.bloodresultsrft"),
    Crf(show_order=250, model="intecomm_subject.bloodresultslft"),
    Crf(show_order=260, model="intecomm_subject.bloodresultslipid"),
    Crf(show_order=270, model="intecomm_subject.hepatitistest"),
    Crf(show_order=280, model="intecomm_subject.malariatest"),
    Crf(show_order=290, model="intecomm_subject.urinedipsticktest"),
    Crf(show_order=360, model="intecomm_subject.concomitantmedication"),
    Crf(show_order=380, model="intecomm_subject.urinepregnancy"),
    Crf(show_order=1000, model="intecomm_subject.pregnancyupdate"),
    name="prn",
)

crfs_unscheduled = FormsCollection(
    Crf(show_order=10, model="intecomm_subject.followupvitals"),
    name="unscheduled",
)

crfs_missed = FormsCollection(
    Crf(show_order=10, model="intecomm_subject.subjectvisitmissed"),
    name="missed",
)
crfs_d1 = FormsCollection(
    Crf(show_order=10, model="intecomm_subject.physicalexam"),
    name="day1",
)
