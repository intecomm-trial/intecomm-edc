from edc_visit_schedule import Crf, FormsCollection

crfs_prn = FormsCollection(
    Crf(show_order=100, model="intecomm_subject.clinicalnote"),
    Crf(show_order=110, model="intecomm_subject.bloodresultsfbc"),
    Crf(show_order=220, model="intecomm_subject.bloodresultsglu"),
    Crf(show_order=230, model="intecomm_subject.bloodresultshba1c"),
    Crf(show_order=240, model="intecomm_subject.bloodresultsrft"),
    Crf(show_order=250, model="intecomm_subject.bloodresultslft"),
    Crf(show_order=260, model="intecomm_subject.bloodresultslipid"),
    Crf(show_order=280, model="intecomm_subject.malariatest"),
    Crf(show_order=290, model="intecomm_subject.urinedipsticktest"),
    Crf(show_order=360, model="intecomm_subject.concomitantmedication"),
    Crf(show_order=380, model="intecomm_subject.urinepregnancy"),
    name="prn",
)

crfs_d1 = FormsCollection(
    Crf(show_order=100, model="intecomm_subject.clinicalreviewbaseline"),
    Crf(show_order=110, model="intecomm_subject.vitals"),
    Crf(show_order=120, model="intecomm_subject.hivinitialreview", required=False),
    Crf(show_order=130, model="intecomm_subject.dminitialreview", required=False),
    Crf(show_order=140, model="intecomm_subject.htninitialreview", required=False),
    Crf(show_order=143, model="intecomm_subject.medications"),
    Crf(show_order=145, model="intecomm_subject.drugrefillhtn", required=False),
    Crf(show_order=150, model="intecomm_subject.drugrefilldm", required=False),
    Crf(show_order=155, model="intecomm_subject.drugrefillhiv", required=False),
    Crf(show_order=165, model="intecomm_subject.hivmedicationadherence", required=False),
    Crf(show_order=170, model="intecomm_subject.dmmedicationadherence", required=False),
    Crf(show_order=185, model="intecomm_subject.htnmedicationadherence", required=False),
    Crf(show_order=190, model="intecomm_subject.otherbaselinedata"),
    Crf(show_order=195, model="intecomm_subject.complicationsbaseline"),
    Crf(show_order=220, model="intecomm_subject.familyhistory"),
    Crf(show_order=240, model="intecomm_subject.icecapa"),
    Crf(show_order=245, model="intecomm_subject.eq5d3l"),
    Crf(show_order=300, model="intecomm_subject.healtheconomicshouseholdhead"),
    Crf(show_order=310, model="intecomm_subject.healtheconomicspatient"),
    Crf(show_order=320, model="intecomm_subject.healtheconomicsassets"),
    Crf(show_order=330, model="intecomm_subject.healtheconomicsproperty"),
    Crf(show_order=340, model="intecomm_subject.healtheconomicsincome"),
    Crf(show_order=400, model="intecomm_subject.nextappointment"),
    name="day1",
)

crfs_followup = FormsCollection(
    Crf(show_order=110, model="intecomm_subject.clinicalreview"),
    Crf(show_order=112, model="intecomm_subject.locationupdate", required=False),
    Crf(show_order=113, model="intecomm_subject.vitals"),
    Crf(show_order=114, model="intecomm_subject.hivinitialreview", required=False),
    Crf(show_order=115, model="intecomm_subject.dminitialreview", required=False),
    Crf(show_order=116, model="intecomm_subject.htninitialreview", required=False),
    Crf(show_order=130, model="intecomm_subject.hivreview", required=False),
    Crf(show_order=140, model="intecomm_subject.dmreview", required=False),
    Crf(show_order=150, model="intecomm_subject.htnreview", required=False),
    Crf(show_order=155, model="intecomm_subject.medications"),
    Crf(show_order=160, model="intecomm_subject.drugrefillhtn", required=False),
    Crf(show_order=170, model="intecomm_subject.drugrefilldm", required=False),
    Crf(show_order=180, model="intecomm_subject.drugrefillhiv", required=False),
    Crf(show_order=185, model="intecomm_subject.hivmedicationadherence", required=False),
    Crf(show_order=190, model="intecomm_subject.dmmedicationadherence", required=False),
    Crf(show_order=195, model="intecomm_subject.htnmedicationadherence", required=False),
    Crf(show_order=200, model="intecomm_subject.complicationsfollowup", required=False),
    Crf(show_order=220, model="intecomm_subject.familyhistory", required=False),
    Crf(show_order=240, model="intecomm_subject.icecapa"),
    Crf(show_order=245, model="intecomm_subject.eq5d3l"),
    Crf(show_order=300, model="intecomm_subject.healtheconomicshouseholdhead", required=False),
    Crf(show_order=310, model="intecomm_subject.healtheconomicspatient", required=False),
    Crf(show_order=320, model="intecomm_subject.healtheconomicsassets", required=False),
    Crf(show_order=330, model="intecomm_subject.healtheconomicsproperty", required=False),
    Crf(show_order=340, model="intecomm_subject.healtheconomicsincome", required=False),
    Crf(show_order=400, model="intecomm_subject.nextappointment"),
    name="followup",
)


crfs_unscheduled = FormsCollection(
    name="unscheduled",
)

crfs_missed = FormsCollection(
    Crf(show_order=10, model="intecomm_subject.subjectvisitmissed"),
    name="missed",
)
