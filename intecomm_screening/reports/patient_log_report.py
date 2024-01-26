import re
from tempfile import mkdtemp

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from edc_auth.constants import PII, PII_VIEW
from edc_consent.utils import get_remove_patient_names_from_countries
from edc_constants.constants import UUID_PATTERN
from edc_identifier.utils import convert_to_human_readable
from edc_pdf_reports import Report
from edc_sites.site import sites
from edc_utils import convert_php_dateformat
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    ParagraphStyle,
    StyleSheet1,
    _baseFontNameB,
    _baseFontNameI,
)
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from intecomm_consent.models import SubjectConsent
from intecomm_screening.models import SubjectScreening


class PatientLogReportError(Exception):
    pass


class PatientLogReport(Report):
    default_page = dict(
        rightMargin=1 * cm,
        leftMargin=1 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        pagesize=A4,
    )

    def __init__(self, patient_log=None, user: User = None, **kwargs):
        super().__init__(**kwargs)
        self.object = patient_log
        if not patient_log.filing_identifier or re.match(
            UUID_PATTERN, patient_log.filing_identifier
        ):
            patient_log.save()
        if not patient_log.patient_log_identifier or re.match(
            UUID_PATTERN, patient_log.patient_log_identifier
        ):
            patient_log.save()
        self.user = user  # a User model instance
        if not user.groups.filter(name=PII):
            raise PatientLogReportError("User does not have permissions to access PII")
        self.image_folder = mkdtemp()
        self.report_filename = f"{self.object.filing_identifier}.pdf"

    def screening(self, attr):
        try:
            obj = SubjectScreening.objects.get(patient_log=self.object)
        except ObjectDoesNotExist:
            value = None
        else:
            value = getattr(obj, attr)
        return value

    def screening_date(self):
        value = self.screening("created")
        if value:
            value = value.strftime(convert_php_dateformat(settings.SHORT_DATETIME_FORMAT))
        return value

    def consent(self, attr):
        try:
            obj = SubjectConsent.objects.get(
                screening_identifier=self.screening("screening_identifier")
            )
        except ObjectDoesNotExist:
            value = None
        else:
            value = getattr(obj, attr)
        return value

    def consent_date(self):
        value = self.consent("created")
        if value:
            value = value.strftime(convert_php_dateformat(settings.SHORT_DATETIME_FORMAT))
        return value

    def add_to_styles(self, styles: StyleSheet1) -> StyleSheet1:
        styles.add(
            ParagraphStyle(name="confidential", fontSize=12, leading=11, alignment=TA_CENTER)
        )
        styles.add(
            ParagraphStyle(name="report_title", fontSize=16, leading=16, alignment=TA_RIGHT)
        )
        styles.add(
            ParagraphStyle(name="field_name_large", alignment=TA_LEFT, fontSize=11, leading=14)
        )
        styles.add(
            ParagraphStyle(
                name="section_heading",
                alignment=TA_LEFT,
                fontSize=11,
                leading=11,
                fontName=_baseFontNameB,
            )
        )
        styles.add(
            ParagraphStyle(
                name="row_instructions",
                fontSize=6,
                leading=7,
                alignment=TA_LEFT,
                fontName=_baseFontNameI,
            )
        )
        styles.add(
            ParagraphStyle(
                name="section_instructions",
                fontSize=10,
                # leading=7,
                alignment=TA_LEFT,
                fontName=_baseFontNameI,
            )
        )

        return styles

    def get_report_story(self, **kwargs):
        story = []
        data = [
            [Paragraph("CONFIDENTIAL", self.styles["confidential"])],
            [Paragraph(" ", self.styles["confidential"])],
            [Paragraph("INTECOMM Patient Reference", self.styles["report_title"])],
        ]
        t = Table(data, colWidths=(9 * cm))
        t.hAlign = "CENTER"
        story.append(t)

        story.append(Spacer(0.1 * cm, 0.5 * cm))

        data = [
            [
                Paragraph(
                    (
                        "KEEP THIS DOCUMENT IN A SECURE LOCATION. FILE SEQUENTIALLY "
                        "ACCORDING TO THE FILE NUMBER. DO NOT WRITE ANY PATIENT HEALTH "
                        "DATA ON THIS DOCUMENT."
                    ),
                    self.styles["line_data_mediumB"],
                ),
                Paragraph("", self.styles["line_label"]),
                [
                    Paragraph("EDC FILE NUMBER:", self.styles["field_name_large"]),
                    Paragraph(
                        self.object.filing_identifier or "", self.styles["field_name_large"]
                    ),
                ],
            ],
        ]
        t = Table(data, colWidths=(8 * cm, None, None), rowHeights=(1.5 * cm))
        t.setStyle(
            TableStyle(
                [
                    ("INNERGRID", (1, 0), (-1, -1), 0.25, colors.black),
                    ("BOX", (2, 0), (-1, -1), 0.25, colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        t.hAlign = "LEFT"
        story.append(t)

        data = [
            [
                Paragraph("", self.styles["line_data_mediumB"]),
                Paragraph("", self.styles["line_label"]),
                [
                    Paragraph("EDC SITE:", self.styles["field_name_large"]),
                    Paragraph(str(self.object.site_id) or "", self.styles["field_name_large"]),
                ],
            ],
        ]
        t = Table(data, colWidths=(8 * cm, None, None), rowHeights=(1.5 * cm))
        t.setStyle(
            TableStyle(
                [
                    ("INNERGRID", (1, 0), (-1, -1), 0.25, colors.black),
                    ("BOX", (2, 0), (-1, -1), 0.25, colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        t.hAlign = "LEFT"
        story.append(t)

        story.append(Spacer(0.1 * cm, 0.25 * cm))

        data = [
            [Paragraph("SECTION ONE", self.styles["section_heading"])],
        ]
        t = Table(data, colWidths=(9 * cm))
        t.hAlign = "LEFT"
        story.append(t)

        story.append(Spacer(0.1 * cm, 0.5 * cm))

        data = [
            (
                [
                    Paragraph("FULL PATIENT NAME:", self.styles["line_data_large"]),
                    Paragraph(
                        "Not available in the EDC",
                        self.styles["row_instructions"],
                    ),
                ],
                [Paragraph(self.legal_name or " ", self.styles["line_data_largest"])],
            ),
            (
                [
                    Paragraph("FAMILIAR NAME:", self.styles["line_data_large"]),
                    Paragraph(
                        "Not available in the EDC",
                        self.styles["row_instructions"],
                    ),
                ],
                [Paragraph(self.familiar_name or " ", self.styles["line_data_largest"])],
            ),
            (
                [Paragraph("INITIALS (2-3 letters):", self.styles["line_data_large"])],
                [Paragraph(self.object.initials or " ", self.styles["line_data_largest"])],
            ),
            (
                [Paragraph("GENDER/AGE:", self.styles["line_data_large"])],
                [
                    Paragraph(
                        f"{self.object.gender or '?'}{self.object.age_in_years or '?'}",
                        self.styles["line_data_largest"],
                    )
                ],
            ),
            (
                [Paragraph("CONTACT:", self.styles["line_data_large"])],
                [
                    Paragraph(
                        (str(self.object.contact_number) or " ")
                        + (
                            f" / {str(self.object.alt_contact_number)}"
                            if str(self.object.alt_contact_number)
                            else ""
                        ),
                        self.styles["line_data_largest"],
                    )
                ],
            ),
            (
                [Paragraph("HOSPITAL IDENTIFIER:", self.styles["line_data_large"])],
                [
                    Paragraph(
                        str(self.object.hospital_identifier) or " ",
                        self.styles["line_data_largest"],
                    )
                ],
            ),
        ]
        t = Table(data, colWidths=(6 * cm, None), rowHeights=(1 * cm))
        t.setStyle(
            TableStyle(
                [
                    ("INNERGRID", (0, 0), (1, 0), 0.25, colors.black),
                    ("INNERGRID", (0, 0), (1, 5), 0.25, colors.black),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        story.append(t)
        data = [
            (
                [
                    Paragraph("Staff name:", self.styles["line_label"]),
                    Paragraph(self.object.user_created, self.styles["line_label"]),
                ],
                [Paragraph("Staff signature:", self.styles["line_label"])],
                [
                    Paragraph("Date completed:", self.styles["line_label"]),
                    Paragraph(
                        self.object.created.strftime(
                            convert_php_dateformat(settings.SHORT_DATETIME_FORMAT)
                        ),
                        self.styles["line_label"],
                    ),
                ],
            ),
        ]
        t = Table(data, rowHeights=(1 * cm))
        t.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        story.append(t)

        story.append(Spacer(0.1 * cm, 0.5 * cm))

        data = [
            [Paragraph("SECTION TWO", self.styles["section_heading"])],
        ]
        t = Table(data, None)
        t.hAlign = "LEFT"
        story.append(t)

        data = [
            [
                Paragraph(
                    "Transcribe the identifiers below from the EDC as they become available.",
                    self.styles["section_instructions"],
                )
            ],
        ]
        t = Table(data)
        t.hAlign = "LEFT"
        story.append(t)

        story.append(Spacer(0.1 * cm, 0.5 * cm))

        data = [
            (
                [
                    Paragraph(
                        "PATIENT LOG IDENTIFIER:",
                        self.styles["line_data_large"],
                    ),
                    Paragraph(
                        "Complete once patient is added to the PATIENT LOG on the EDC",
                        self.styles["row_instructions"],
                    ),
                ],
                [
                    Paragraph(
                        convert_to_human_readable(self.object.patient_log_identifier) or " ",
                        self.styles["line_data_largest"],
                    )
                ],
                [
                    Paragraph("Initials and date", self.styles["line_label"]),
                    Paragraph(
                        self.object.user_created,
                        self.styles["line_label"],
                    ),
                    Paragraph(
                        self.object.created.strftime(
                            convert_php_dateformat(settings.SHORT_DATETIME_FORMAT)
                        ),
                        self.styles["line_label"],
                    ),
                ],
            ),
            (
                [
                    Paragraph("SCREENING IDENTIFIER:", self.styles["line_data_large"]),
                    Paragraph(
                        "Complete once subject's SCREENING FORM is submitted on the EDC",
                        self.styles["row_instructions"],
                    ),
                ],
                [
                    Paragraph(
                        convert_to_human_readable(self.object.screening_identifier) or " ",
                        self.styles["line_data_largest"],
                    )
                ],
                [
                    Paragraph("Initials and date", self.styles["line_label"]),
                ],
            ),
            (
                [
                    Paragraph("SUBJECT IDENTIFIER:", self.styles["line_data_large"]),
                    Paragraph(
                        "Complete once subject's INFORMED CONSENT FORM is submitted "
                        "on the EDC",
                        self.styles["row_instructions"],
                    ),
                ],
                [
                    Paragraph(
                        self.object.subject_identifier or " ", self.styles["line_data_largest"]
                    )
                ],
                [Paragraph("Initials and date", self.styles["line_label"])],
            ),
            (
                [
                    Paragraph("GROUP IDENTIFIER:", self.styles["line_data_large"]),
                    Paragraph(
                        "Complete once participant's GROUP has randomized on the EDC",
                        self.styles["row_instructions"],
                    ),
                ],
                [
                    Paragraph(
                        self.object.group_identifier or " ", self.styles["line_data_largest"]
                    )
                ],
                [Paragraph("Initials and date", self.styles["line_label"])],
            ),
        ]
        t = Table(data, colWidths=(6 * cm, None, 3 * cm), rowHeights=(1.5 * cm))
        t.setStyle(
            TableStyle(
                [
                    ("INNERGRID", (0, 0), (1, 0), 0.25, colors.black),
                    ("INNERGRID", (0, 0), (2, 3), 0.25, colors.black),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        story.append(t)

        story.append(Spacer(0.1 * cm, 0.5 * cm))

        data = [
            [Paragraph("SECTION THREE", self.styles["section_heading"])],
        ]
        t = Table(data, colWidths=(9 * cm))
        t.hAlign = "LEFT"
        story.append(t)

        data = [
            [
                Paragraph(
                    "Complete this section after group randomization or at "
                    "a time when it is known the subject will NOT advance to "
                    "randomization.",
                    self.styles["section_instructions"],
                )
            ]
        ]
        t = Table(data)
        t.hAlign = "LEFT"
        story.append(t)

        story.append(Spacer(0.1 * cm, 0.5 * cm))

        data = [
            [
                Paragraph(
                    "THE ABOVE DATA HAS BEEN INDEPENDENTLY VERIFIED AGAINST THE EDC",
                    self.styles["line_data_large"],
                )
            ],
        ]
        t = Table(data)
        t.hAlign = "LEFT"
        story.append(t)

        data = [
            (
                [Paragraph("Staff name:", self.styles["line_label"])],
                [Paragraph("Staff signature:", self.styles["line_label"])],
                [Paragraph("Date verified:", self.styles["line_label"])],
            ),
        ]
        t = Table(data, rowHeights=(1 * cm))
        t.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        story.append(t)
        return story

    @property
    def familiar_name(self) -> str | None:
        if self.has_pii_perms():
            return self.object.familiar_name
        return ""

    @property
    def legal_name(self) -> str | None:
        if self.has_pii_perms():
            return self.object.legal_name
        return ""

    def has_pii_perms(self) -> bool:
        has_pii_perms: bool | None = None
        user_sites = set([s.id for s in self.user.userprofile.sites.all()])
        for country in get_remove_patient_names_from_countries():
            country_sites = set(
                [s.site_id for s in sites.get_by_country(country, aslist=True)]
            )
            if user_sites & country_sites:
                has_pii_perms = False
                break
        if has_pii_perms is None and self.user.groups.filter(name__in=[PII, PII_VIEW]):
            has_pii_perms = True
        return has_pii_perms
