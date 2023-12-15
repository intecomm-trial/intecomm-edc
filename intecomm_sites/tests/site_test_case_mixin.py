from edc_sites.site import sites


class SiteTestCaseMixin:
    default_country = "tz"

    @property
    def default_sites(self):
        return sites.get_by_country(self.default_country)

    @property
    def site_names(self):
        return [s.name for s in self.default_sites]

    @property
    def default_all_sites(self):
        return sites.all()
