from intecomm_group.models import PatientGroup as BasePatientGroup


class PatientGroup(BasePatientGroup):
    def __str__(self):
        status = " (R)" if self.randomized else ""
        return f"{self.name.upper()}{status}"

    class Meta:
        proxy = True
