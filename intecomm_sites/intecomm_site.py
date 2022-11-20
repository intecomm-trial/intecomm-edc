from edc_sites.single_site import SingleSite


class IntecommSite(SingleSite):
    def __init__(self, site_id, name, *, health_facility_type: str = None, **kwargs):
        self.health_facility_type = health_facility_type
        super().__init__(site_id, name, **kwargs)

    def __str__(self):
        return f"{self.name} {self.health_facility_type}"

    @property
    def site(self):
        lst = super().site
        lst.append(self.health_facility_type)
        return lst

    @property
    def as_dict(self):
        dct = super().as_dict()
        dct.update(health_facility_type=self.health_facility_type)
        return dct

    def save(self, force_insert=False, force_update=False):
        raise NotImplementedError("IntecommSite cannot be saved.")

    def delete(self):
        raise NotImplementedError("IntecommSite cannot be deleted.")
