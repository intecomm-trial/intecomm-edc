from django.core.management import BaseCommand

from intecomm_subject.utils import update_current_conditions


class Command(BaseCommand):
    def __init__(self, **kwargs):
        self.site_ids: list[int] = []
        super().__init__(**kwargs)

    def handle(self, *args, **options):
        update_current_conditions(delete_all=True)
