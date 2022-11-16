from edc_appointment.constants import (
    CANCELLED_APPT,
    COMPLETE_APPT,
    IN_PROGRESS_APPT,
    NEW_APPT,
)
from edc_constants.constants import CLOSED, COMPLETE, NEW, OPEN
from edc_visit_tracking.constants import SCHEDULED
from intecomm_form_validators import DISSOLVED, IN_FOLLOWUP, RECRUITING

from .constants import ATTENDED

GROUP_STATUS_CHOICES = (
    (NEW, "New"),
    (RECRUITING, "Recruiting"),
    (COMPLETE, "Complete/Ready"),
    (IN_FOLLOWUP, "In followup"),
    (DISSOLVED, "Dissolved"),
)

LOCATION_STATUS = ((OPEN, "Open"), (CLOSED, "Closed"))

MEETING_STATUS = (
    (SCHEDULED, "Scheduled"),
    (ATTENDED, "Attended"),
)

APPT_STATUS = (
    (NEW_APPT, "Scheduled"),
    (IN_PROGRESS_APPT, "In Progress"),
    (COMPLETE_APPT, "Done"),
    (CANCELLED_APPT, "Cancelled"),
)
