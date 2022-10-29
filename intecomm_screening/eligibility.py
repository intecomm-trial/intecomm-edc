from edc_constants.constants import DM, FEMALE, HIV, HTN, MALE, NO, NOT_APPLICABLE, YES
from edc_screening.fc import FC
from edc_screening.screening_eligibility import ScreeningEligibility as Base
from edc_vitals import calculate_avg_bp


class ScreeningEligibility(Base):
    def __init__(self, **kwargs):
        self._qualifying_conditions = []
        self.age_in_years = None
        self.art_adherent = None
        self.art_stable = None
        self.art_unchanged_3m = None
        self.dia_blood_pressure_avg = None
        self.dia_blood_pressure_one = None
        self.dia_blood_pressure_two = None
        self.dm_complications = None
        self.dm_dx = None
        self.dm_dx_6m = None
        self.excluded_by_bp_history = None
        self.excluded_by_gluc_history = None
        self.gender = None
        self.hiv_dx = None
        self.hiv_dx_6m = None
        self.htn_complications = None
        self.htn_dx = None
        self.htn_dx_6m = None
        self.in_care_6m = None
        self.lives_nearby = None
        self.pregnant = None
        self.requires_acute_care = None
        self.staying_nearby_6 = None
        self.sys_blood_pressure_avg = None
        self.sys_blood_pressure_one = None
        self.sys_blood_pressure_two = None
        self.unsuitable_for_study = None
        super().__init__(**kwargs)

    def set_fld_attrs_on_self(self):
        super().set_fld_attrs_on_self()

    def get_required_fields(self) -> dict[str, FC]:
        return {
            "age_in_years": FC(range(18, 120), "age<18"),
            "art_adherent": None,
            "art_stable": None,
            "art_unchanged_3m": None,
            "dia_blood_pressure_avg": None,
            "dia_blood_pressure_one": None,
            "dia_blood_pressure_two": None,
            "dm_complications": None,
            "dm_dx": None,
            "dm_dx_6m": None,
            "excluded_by_bp_history": FC(NO, "BP history"),
            "excluded_by_gluc_history": FC(NO, "Glucose history"),
            "gender": FC([MALE, FEMALE], "gender invalid"),
            "hiv_dx": None,
            "hiv_dx_6m": None,
            "htn_complications": None,
            "htn_dx": None,
            "htn_dx_6m": None,
            "in_care_6m": FC(YES, "Not in care for 6m"),
            "lives_nearby": FC(YES, "Does not live in catchment area"),
            "pregnant": FC([NO, NOT_APPLICABLE], "Pregnant"),
            "requires_acute_care": FC(NO, "Glucose history"),
            "staying_nearby_6": FC(YES, "Unable/Unwilling to stay in catchment area"),
            "sys_blood_pressure_avg": None,
            "sys_blood_pressure_one": None,
            "sys_blood_pressure_two": None,
            "unsuitable_for_study": FC(NO, "Unsuitable for study"),
        }

    def assess_eligibility(self) -> None:
        if not self.qualifying_conditions:
            self.eligible = NO
            self.reasons_ineligible.update(no_conditions="No conditions (HIV, DM, HTN)")
        if HIV in self.qualifying_conditions:
            if self.art_unchanged_3m == NO:
                self.eligible = NO
                self.reasons_ineligible.update(art_unchanged_3m="ART changed within 3m")
            if self.art_stable == NO:
                self.eligible = NO
                self.reasons_ineligible.update(art_unchanged_3m="ART unstable")
            if self.art_adherent == NO:
                self.eligible = NO
                self.reasons_ineligible.update(art_unchanged_3m="ART not adherent")
        if DM in self.qualifying_conditions and self.dm_complications == YES:
            self.eligible = NO
            self.reasons_ineligible.update(dm_complications="DM complication")
        if HTN in self.qualifying_conditions and self.htn_complications == YES:
            self.eligible = NO
            self.reasons_ineligible.update(htn_complications="HTN complication")
        sys_blood_pressure_avg, dia_blood_pressure_avg = calculate_avg_bp(
            sys_blood_pressure_one=self.sys_blood_pressure_one,
            sys_blood_pressure_two=self.sys_blood_pressure_two,
            dia_blood_pressure_one=self.dia_blood_pressure_one,
            dia_blood_pressure_two=self.dia_blood_pressure_two,
        )
        if (
            sys_blood_pressure_avg is not None
            and dia_blood_pressure_avg is not None
            and (sys_blood_pressure_avg > 140 or dia_blood_pressure_avg > 90)
        ):
            self.eligible = NO
            self.reasons_ineligible.update(bp_high="BP high")

    @property
    def qualifying_conditions(self):
        if not self._qualifying_conditions:
            if self.hiv_dx == YES and self.hiv_dx_6m == YES:
                self._qualifying_conditions.append(HIV)
            if self.dm_dx == YES and self.dm_dx_6m == YES:
                self._qualifying_conditions.append(DM)
            if self.htn_dx == YES and self.htn_dx_6m == YES:
                self._qualifying_conditions.append(HTN)
        return self._qualifying_conditions
