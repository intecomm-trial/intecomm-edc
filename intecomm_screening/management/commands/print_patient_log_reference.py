import os
from getpass import getpass

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand, CommandError
from edc_sites.site import sites
from edc_utils import get_utcnow
from tqdm import tqdm

from intecomm_screening.models import PatientLog, PatientLogReportPrintHistory
from intecomm_screening.reports import PatientLogReport


class Command(BaseCommand):
    def __init__(self, **kwargs):
        self.site_ids: list[int] = []
        super().__init__(**kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--path",
            dest="path",
            default=False,
            help="export path",
        )

        parser.add_argument(
            "--country",
            dest="country",
            default="",
            help="only export data for country",
        )

        parser.add_argument(
            "--site",
            dest="site_ids",
            default="",
            help="only export data for site",
        )

    def handle(self, *args, **options):
        user = self.validate_user_perms_or_raise()
        export_path = os.path.expanduser(options["path"])
        if not export_path or not os.path.exists(export_path):
            raise CommandError(f"Path does not exist. Got `{export_path}`")
        site_ids = [options["site_ids"]] if options["site_ids"] else []
        countries = [options["country"]] if options["country"] else []
        self.site_ids = site_ids or self.get_site_ids(countries=countries)
        queryset = PatientLog.objects.filter(site__in=self.site_ids).order_by(
            "site", "filing_identifier"
        )
        total = queryset.count()
        for obj in tqdm(queryset, total=total):
            PatientLogReport(patient_log=obj, user=user).render_to_file(
                export_path, verbose=False
            )
            PatientLogReportPrintHistory.objects.create(
                patient_log_identifier=obj.patient_log_identifier,
                printed_datetime=get_utcnow(),
                printed_user=user.username,
            )
            obj.printed = True
            obj.save(update_fields=["printed"])

    @staticmethod
    def validate_user_perms_or_raise() -> User:
        username = input("Username:")
        passwd = getpass("Password for " + username + ":")
        try:
            user = User.objects.get(username=username, is_superuser=False, is_active=True)
        except ObjectDoesNotExist:
            raise CommandError("Invalid username or password.")
        if not user.check_password(passwd):
            raise CommandError("Invalid username or password.")
        if not user.groups.filter(name="EXPORT_PII").exists():
            raise CommandError("You are not authorized to export/print sensitive data.")
        return user

    @staticmethod
    def get_site_ids(
        countries: list[str] | None,
    ) -> list[int]:
        site_ids = []
        for country in countries or []:
            for single_site in sites.get_by_country(country):
                site_ids.append(single_site.site_id)
        return site_ids
