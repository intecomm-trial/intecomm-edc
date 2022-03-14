from django.core.management import color_style
from edc_visit_schedule import site_visit_schedules

style = color_style()

from .visit_schedule import visit_schedule

site_visit_schedules.register(visit_schedule)
