from __future__ import annotations

from typing import Type

import inflect
from django.db import models
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from ...choices import DISCLOSURE, IMPACT_SEVERITY, IMPACT_STATUS

inflect = inflect.engine()


def disclosure_model_mixin_factory(
    *prefixes: str,
) -> Type[models.Model]:
    """Returns an abstract model class"""

    class AbstractModel(models.Model):
        class Meta:
            abstract = True

    attrs = {}
    for prefix in prefixes:
        do_str = "Do any of" if inflect.singular_noun(prefix) else "Does"
        attrs.update(
            {
                prefix: models.CharField(
                    verbose_name=(
                        f"{do_str} your {prefix.upper()} know about your participation in the "
                        "study?"
                    ),
                    max_length=25,
                    choices=YES_NO_NA,
                ),
                f"{prefix}_disclosure": models.CharField(
                    verbose_name="If Yes, how did they find out?",
                    max_length=25,
                    choices=DISCLOSURE,
                    default=NOT_APPLICABLE,
                    help_text=(
                        "(e.g., they saw study material, or I had to disclose DM/HTN/HIV"
                    ),
                ),
            }
        )

    for name, fld_cls in attrs.items():
        AbstractModel.add_to_class(name, fld_cls)
    return AbstractModel


def impact_model_mixin_factory(
    *prefixes: str, lead_verbose_name: str | None = None
) -> Type[models.Model]:
    """Returns an abstract model class"""

    class AbstractModel(models.Model):
        class Meta:
            abstract = True

    attrs = {}
    for prefix in prefixes:
        attrs.update(
            {
                f"{prefix}_impact": models.CharField(
                    verbose_name=lead_verbose_name or f"... with your {prefix}?",
                    max_length=25,
                    choices=YES_NO_NA,
                ),
                f"{prefix}_impact_severity": models.CharField(
                    verbose_name="Severity of impact",
                    max_length=25,
                    choices=IMPACT_SEVERITY,
                    default=NOT_APPLICABLE,
                ),
                f"{prefix}_impact_status": models.CharField(
                    verbose_name="Status of impact",
                    max_length=25,
                    choices=IMPACT_STATUS,
                    default=NOT_APPLICABLE,
                ),
                f"{prefix}_impact_help": models.CharField(
                    verbose_name="Would you like help",
                    max_length=25,
                    choices=YES_NO_NA,
                    default=NOT_APPLICABLE,
                ),
                f"{prefix}_impact_referal": models.CharField(
                    verbose_name="Has the participant been referred for further help",
                    max_length=25,
                    choices=YES_NO_NA,
                    default=NOT_APPLICABLE,
                ),
            }
        )

    for name, fld_cls in attrs.items():
        AbstractModel.add_to_class(name, fld_cls)
    return AbstractModel
