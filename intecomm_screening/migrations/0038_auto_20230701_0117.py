# Generated by Django 4.2.1 on 2023-06-30 22:17
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations
from django.db.migrations import RunPython
from edc_constants.constants import NO, NOT_APPLICABLE, TBD, YES
from edc_list_data import PreloadData
from tqdm import tqdm

from intecomm_lists.list_data import list_data


def update_willing_to_screen(apps, schema_editor):
    data = {
        k: v for k, v in list_data.items() if k == ("intecomm_lists.screeningrefusalreasons")
    }
    PreloadData(list_data=data, apps=apps)
    patientlog_cls = apps.get_model("intecomm_screening.patientlog")
    subjectscreening_cls = apps.get_model("intecomm_screening.subjectscreening")
    screeningrefusalreasons_cls = apps.get_model("intecomm_lists.screeningrefusalreasons")
    # may fail here if post-migrate needs to run
    not_applicable = screeningrefusalreasons_cls.objects.get(name=NOT_APPLICABLE)
    qs = patientlog_cls.objects.all()
    for patientlog in tqdm(qs, total=qs.count()):
        try:
            subjectscreening_cls.objects.get(patient_log_id=patientlog.id)
        except ObjectDoesNotExist:
            if patientlog.screening_refusal_reason:
                patientlog.willing_to_screen = NO
            else:
                patientlog.willing_to_screen = TBD
                patientlog.screening_refusal_reason = not_applicable
        else:
            patientlog.willing_to_screen = YES
            patientlog.screening_refusal_reason = not_applicable
        patientlog.save_base(update_fields=["willing_to_screen", "screening_refusal_reason"])


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_lists", "0007_arvdrugs_extra_value_arvregimens_extra_value_and_more"),
        ("intecomm_screening", "0037_alter_consentrefusal_screening_identifier_and_more"),
    ]

    operations = [RunPython(update_willing_to_screen)]
