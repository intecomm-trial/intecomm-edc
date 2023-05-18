from __future__ import annotations

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from edc_constants.constants import MULTI_MORBIDITY
from edc_dx import get_diagnosis_labels_prefixes
from intecomm_form_validators import RECRUITING

from ..utils import PatientGroupRatioError, verify_patient_group_ratio_raise
from .patient_group_appointment import PatientGroupAppointment
from .patient_group_meeting import PatientGroupMeeting


@receiver(
    post_save,
    weak=False,
    dispatch_uid="update_patientgroup_on_post_save",
)
def update_patientgroup_on_post_save(sender, instance, raw, update_fields, **kwargs):
    """Check ratio.

    Careful, this will fire before the m2m signal so may not be working with
    up-to-date patient_log instances.
    """
    if (
        not raw
        and not update_fields
        and instance._meta.label_lower.split(".")[1] == "patientgroup"
    ):
        try:
            _, _, ratio = verify_patient_group_ratio_raise(
                instance.patients.all(), raise_on_outofrange=True
            )
        except PatientGroupRatioError:
            if not instance.bypass_group_ratio:
                instance.status = RECRUITING
            _, _, ratio = verify_patient_group_ratio_raise(
                instance.patients.all(), raise_on_outofrange=False
            )
        instance.ratio = ratio
        instance.save_base(update_fields=["ratio", "status"])


@receiver(
    m2m_changed,
    weak=False,
    dispatch_uid="update_patientgroup_patients_from_patientlog_m2ms_on_m2m_changed",
)
def update_patientgroup_patients_from_patientlog_m2ms_on_m2m_changed(
    action, instance, sender, model, pk_set, **kwargs
):
    if model._meta.label_lower == "intecomm_screening.patientlog":
        label_lower = sender._meta.label_lower
        patient_log_cls = django_apps.get_model("intecomm_screening.patientlog")
        conditions = get_diagnosis_labels_prefixes()
        conditions.append(MULTI_MORBIDITY)
        dirty = False
        if action == "post_add":
            for cond in conditions:
                if label_lower == f"intecomm_group.patientgroup_{cond.lower()}_patients":
                    objs = [
                        patient for patient in patient_log_cls.objects.filter(pk__in=pk_set)
                    ]
                    instance.patients.add(*objs)
                    dirty = True
        elif action == "post_remove":
            for cond in conditions:
                if label_lower == f"intecomm_group.patientgroup_{cond.lower()}_patients":
                    objs = [
                        patient for patient in patient_log_cls.objects.filter(pk__in=pk_set)
                    ]
                    instance.patients.remove(*objs)
                    dirty = True
        if dirty:
            instance.status = RECRUITING
            _, _, ratio = verify_patient_group_ratio_raise(
                instance.patients.all(), raise_on_outofrange=False
            )
            instance.ratio = ratio
            instance.save_base(update_fields=["ratio", "status"])


@receiver(
    post_save,
    dispatch_uid="create_or_update_refills_on_post_save",
    sender=PatientGroupAppointment,
)
def create_or_update_patientgroup_meeting_on_post_save(
    sender, instance, raw, created, update_fields, **kwargs
):
    if not raw:
        try:
            PatientGroupMeeting.objects.get(patient_group_appointment=instance)
        except ObjectDoesNotExist:
            PatientGroupMeeting.objects.create(
                patient_group_appointment=instance,
            )
