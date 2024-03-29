# Generated by Django 4.2.6 on 2023-11-20 11:59
from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import migrations
from django.db.migrations import RunPython
from edc_constants.constants import INCOMPLETE
from edc_he.calculators import convert_to_sq_meters
from edc_utils import get_utcnow
from tqdm import tqdm

if TYPE_CHECKING:
    from decimal import Decimal


def get_calculated_land_surface_area(obj) -> Decimal | None:
    """Returns land surface area converted to m2.

    Reproduced from: edc_he.model_mixins.property_model_mixin
    """
    calculated_land_surface_area = None
    if obj.land_surface_area and obj.land_surface_area_units:
        calculated_land_surface_area = convert_to_sq_meters(
            area=obj.land_surface_area,
            area_units=obj.land_surface_area_units,
        )
    return calculated_land_surface_area


def update_calculated_land_surface_area(apps, schema_editor):
    he_property_model_cls = apps.get_model("intecomm_subject.healtheconomicsproperty")
    qs = he_property_model_cls.objects.all()
    total = qs.count()
    print(f"\nProcessing {total} HE Property CRFs ...")
    for obj in tqdm(qs, total=total):
        if obj.land_surface_area:
            obj.calculated_land_surface_area = get_calculated_land_surface_area(obj)
            obj.modified = get_utcnow()
            obj.user_modified = __name__ if len(__name__) <= 50 else f"{__name__[:46]} ..."

            if obj.site_id < 200:  # Uganda
                obj.crf_status = INCOMPLETE
                migration_comment = (
                    "[CRF marked INCOMPLETE by system at: "
                    f"{obj.modified.strftime('%Y-%m-%dT%H:%M:%SZ')} "
                    f"({__name__}) (see also Redmine ticket #683)]. "
                    "Please review CRF and save."
                )
                obj.crf_status_comments = (
                    f"{obj.crf_status_comments} \n\n{migration_comment}"
                    if obj.crf_status_comments
                    else migration_comment
                )
            obj.save_base(
                update_fields=[
                    "calculated_land_surface_area",
                    "modified",
                    "user_modified",
                    "crf_status",
                    "crf_status_comments",
                ]
            )
    print("Done.")


class Migration(migrations.Migration):
    dependencies = [
        (
            "intecomm_subject",
            "0125_healtheconomicsproperty_calculated_land_surface_area_and_more",
        ),
    ]

    operations = [RunPython(update_calculated_land_surface_area)]
