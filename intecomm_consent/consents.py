from edc_consent.consent_definition import ConsentDefinition
from edc_consent.site_consents import site_consents
from edc_constants.constants import FEMALE, MALE
from edc_protocol.research_protocol_config import ResearchProtocolConfig


def opts() -> dict:
    return dict(
        version="1",
        start=ResearchProtocolConfig().study_open_datetime,
        end=ResearchProtocolConfig().study_close_datetime,
        age_min=18,
        age_is_adult=18,
        age_max=110,
        gender=[MALE, FEMALE],
    )


cdef_tz_v1 = ConsentDefinition(
    proxy_model="intecomm_consent.subjectconsenttz",
    country="tanzania",
    **opts(),
)
cdef_ug_v1 = ConsentDefinition(
    proxy_model="intecomm_consent.subjectconsentug",
    country="uganda",
    **opts(),
)

site_consents.register(cdef_tz_v1)
site_consents.register(cdef_ug_v1)
