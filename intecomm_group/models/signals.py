from __future__ import annotations

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from edc_constants.constants import COMPLETE, DM, HIV, HTN

from ..utils import verify_patient_group_ratio_raise
from .patient_group import PatientGroup
from .patient_group_appointment import PatientGroupAppointment
from .patient_group_meeting import PatientGroupMeeting


@receiver(
    post_save,
    weak=False,
    sender=PatientGroup,
    dispatch_uid="update_patient_group_ratio_on_post_save",
)
def update_patient_group_ratio_on_post_save(sender, instance, raw, update_fields, **kwargs):
    if not raw and not update_fields:
        raise_on_outofrange = True if instance.status == COMPLETE else False
        ncd, hiv, ratio = verify_patient_group_ratio_raise(
            instance.patients.all(), raise_on_outofrange=raise_on_outofrange
        )
        instance.ratio = ratio
        instance.save_base(update_fields=["ratio"])


@receiver(
    post_save,
    dispatch_uid="create_or_update_refills_on_post_save",
    sender=PatientGroupAppointment,
)
def create_or_update_patient_group_meeting_on_post_save(
    sender, instance, raw, created, update_fields, **kwargs
):
    if not raw:
        try:
            PatientGroupMeeting.objects.get(patient_group_appointment=instance)
        except ObjectDoesNotExist:
            PatientGroupMeeting.objects.create(
                patient_group_appointment=instance,
            )


@receiver(
    m2m_changed,
    # sender=PatientGroup,
    weak=False,
    dispatch_uid="update_patients_from_m2ms_on_m2m_changed",
)
def update_patients_from_m2ms_on_m2m_changed(
    action, instance, sender, model, pk_set, **kwargs
):
    if model._meta.label_lower == "intecomm_screening.patientlog":
        label_lower = sender._meta.label_lower
        patient_log_cls = django_apps.get_model("intecomm_screening.patientlog")
        if action == "post_add":
            for cond in [HIV, DM, HTN, "multi"]:
                if label_lower == f"intecomm_group.patientgroup_{cond.lower()}_patients":
                    objs = [
                        patient for patient in patient_log_cls.objects.filter(pk__in=pk_set)
                    ]
                    instance.patients.add(*objs)
        elif action == "post_remove":
            for cond in [HIV, DM, HTN, "multi"]:
                if label_lower == f"intecomm_group.patientgroup_{cond.lower()}_patients":
                    objs = [
                        patient for patient in patient_log_cls.objects.filter(pk__in=pk_set)
                    ]
                    instance.patients.remove(*objs)
