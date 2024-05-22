from edc_appointment.constants import COMPLETE_APPT, IN_PROGRESS_APPT, INCOMPLETE_APPT
from edc_appointment.models import Appointment
from edc_sites.site import sites as site_sites
from edc_utils import get_utcnow
from intecomm_rando.constants import FACILITY_ARM
from intecomm_rando.utils import get_assignment_for_subject

sites = {}

for site in site_sites.get_by_country("uganda", aslist=True):
    isodays = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
    for obj in Appointment.objects.filter(
        appt_status__in=[IN_PROGRESS_APPT, INCOMPLETE_APPT, COMPLETE_APPT],
        appt_datetime__lt=get_utcnow(),
        site__id=site.site_id,
    ):
        if get_assignment_for_subject(obj.subject_identifier) == FACILITY_ARM:
            isodays[obj.appt_datetime.isoweekday()] += 1
    sites.update({site.site_id: isodays})
