from django.core.management import BaseCommand

from intecomm_reports.utils import update_diagnoses_model


class Command(BaseCommand):
    def __init__(self, **kwargs):
        self.site_ids: list[int] = []
        super().__init__(**kwargs)

    def handle(self, *args, **options):
        update_diagnoses_model(delete_all=True)
