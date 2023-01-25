from django.db import models
from edc_model.models import BaseUuidModel

from ...model_mixins import CrfModelMixin
from .model_factories import disclosure_model_mixin_factory, impact_model_mixin_factory


class SocialHarms(
    disclosure_model_mixin_factory("partner", "family", "friends", "coworkers"),
    impact_model_mixin_factory(
        "partner",
        "family",
        "friends",
        "coworkers",
        "healthcare",
    ),
    impact_model_mixin_factory(
        "other_service", lead_verbose_name="... with any other health service"
    ),
    impact_model_mixin_factory(
        "employment",
        "insurance",
    ),
    impact_model_mixin_factory(
        "other", lead_verbose_name="... with any other aspect of your life"
    ),
    CrfModelMixin,
    BaseUuidModel,
):
    other_service_impact_description = models.CharField(
        verbose_name="Please describe ...", max_length=50, null=True, blank=True
    )

    other_impact_description = models.CharField(
        verbose_name="Please describe ...", max_length=50, null=True, blank=True
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Social Harms"
        verbose_name_plural = "Social Harms"
