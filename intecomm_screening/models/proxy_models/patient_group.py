from intecomm_group.models import PatientGroup as BasePatientGroup


class PatientGroup(BasePatientGroup):
    def __str__(self):
        return self.name.upper()

    class Meta:
        proxy = True
