from django.contrib import admin, messages
from edc_utils import get_utcnow

from ..models import PatientLogReportPrintHistory
from ..reports import PatientLogReport, PatientLogReportError


@admin.action(description="Print patient reference")
def render_pdf_action(modeladmin, request, queryset, **kwargs):  # noqa
    report = None
    if queryset.count() > 1:
        messages.add_message(
            request, messages.ERROR, "Select only one patient to print and try again"
        )
    else:
        for obj in queryset:
            try:
                report = PatientLogReport(
                    patient_log=obj, user=request.user
                ).render_to_response()
            except PatientLogReportError as e:
                messages.add_message(request, messages.ERROR, str(e))
                break
            PatientLogReportPrintHistory.objects.create(
                patient_log_identifier=obj.patient_log_identifier,
                printed_datetime=get_utcnow(),
                printed_user=request.user.username,
            )
            obj.printed = True
            obj.save(update_fields=["printed"])
            messages.add_message(
                request,
                messages.SUCCESS,
                f"Successfully printed patient reference for {obj.patient_log_identifier}.",
            )
    return report
