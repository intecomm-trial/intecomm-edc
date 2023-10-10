from django.core.management import color_style
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from .visit_schedule import visit_schedule

style = color_style()

site_visit_schedules.register(visit_schedule)
