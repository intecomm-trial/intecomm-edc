from intecomm_facility.models import HealthFacility as Base


# TODO: remove, not used. Remove after migrations are squashed/reset
class HealthFacility(Base):
    class Meta:
        proxy = True
