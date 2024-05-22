from django.core.management import BaseCommand

from intecomm_subject.utils import recalculate_dx_calculated_date


class Command(BaseCommand):
    def __init__(self, **kwargs):
        self.site_ids: list[int] = []
        super().__init__(**kwargs)

    def handle(self, *args, **options):
        recalculate_dx_calculated_date()
