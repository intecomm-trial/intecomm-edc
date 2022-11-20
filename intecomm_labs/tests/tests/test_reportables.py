from tempfile import mkdtemp

from django.test import TestCase
from edc_reportable import ParserError, site_reportables


class TestReportables(TestCase):
    def test(self):
        try:
            pass
            # from intecomm_labs import reportables
        except ParserError:
            self.fail("ParserError unexpectedly raised.")
        self.assertIsNotNone(site_reportables.get("intecomm"))
        filename1, filename2 = site_reportables.to_csv("intecomm", path=mkdtemp())
        print(filename1)
        print(filename2)
