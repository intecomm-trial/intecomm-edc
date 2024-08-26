#!/usr/bin/env python
from edc_test_settings.func_main import func_main2

if __name__ == "__main__":
    project_tests = [
        "intecomm_auth.tests",
        "intecomm_ae.tests",
        "intecomm_dashboard.tests",
        "intecomm_edc.tests",
        "intecomm_labs.tests",
        "intecomm_lists.tests",
        "intecomm_prn.tests",
        "intecomm_group.tests",
        "intecomm_screening.tests",
        "intecomm_subject.tests",
        "intecomm_consent.tests",
        "intecomm_visit_schedule.tests",
        "intecomm_form_validators.tests",
        "intecomm_rando.tests",
        "intecomm_eligibility.tests",
    ]

    func_main2("tests.test_settings", *project_tests)
