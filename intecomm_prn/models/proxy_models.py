from intecomm_screening.models import PatientGroup as BasePatientGroup
from intecomm_screening.models import PatientLog as BasePatientLog


class PatientGroup(BasePatientGroup):
    class Meta:
        proxy = True


class PatientLog(BasePatientLog):
    class Meta:
        proxy = True
