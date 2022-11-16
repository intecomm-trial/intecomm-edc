from __future__ import annotations

from edc_constants.constants import COMPLETE

from ..exceptions import PatientGroupError
from .patient_group import PatientGroup


def add_to_group(instance, commit: bool | None = None):
    commit = True if commit is None else commit
    to_group = instance.patient_group
    if through_qs := instance.patientgroup_set.through.objects.filter(
        patientlog_id=instance.id
    ):
        if to_group and to_group.id != through_qs.first().patientgroup_id:
            if not instance.patient_group.patients.filter(name=instance.name).exists():
                if commit:
                    instance.patient_group.patients.add(instance)
            else:
                raise PatientGroupError(
                    "Cannot add patient to group. Already a member of this group"
                )
    else:
        if commit:
            instance.patient_group.patients.add(instance)


def remove_from_group(instance, commit: bool | None = None):
    """Updates patient_group.patients(m2m) using
    patient_log.patient_group(fk).
    """
    commit = True if commit is None else commit
    to_group = instance.patient_group
    if through_qs := instance.patientgroup_set.through.objects.filter(
        patientlog_id=instance.id
    ):
        ids = [obj.patientgroup_id for obj in through_qs]
        if from_patient_group_qs := PatientGroup.objects.filter(id__in=ids):
            if to_group and from_patient_group_qs.first().id == to_group.id:
                pass
            else:
                if COMPLETE in [obj.status for obj in from_patient_group_qs]:
                    raise PatientGroupError(
                        "Cannot remove patient from group. See patient group "
                        f"{from_patient_group_qs.first()}."
                    )
                for obj in from_patient_group_qs:
                    if commit:
                        obj.patients.remove(instance)
