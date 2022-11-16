from intecomm_group.models import PatientGroup as BasePatientGroup


class PatientGroup(BasePatientGroup):
    class Meta:
        proxy = True
