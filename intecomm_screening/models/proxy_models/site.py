from django.contrib.sites.models import Site as Base


class Site(Base):
    def __str__(self):
        return self.name.replace("_", " ").title()

    class Meta:
        proxy = True
