from __future__ import annotations

from dataclasses import dataclass, field

from edc_sites.single_site import SingleSite


@dataclass(init=True)
class IntecommSite(SingleSite):
    health_facility_type: str = field(kw_only=True, default="")
    clinic_days: list[int] = field(kw_only=True, default_factory=list)

    def __str__(self):
        return f"{self.description} {self.health_facility_type.upper()} ({self.site_id})"
