from edc_list_data.model_mixins import ListModelMixin


class ArvDrugs(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Arv Drugs"
        verbose_name_plural = "Arv Drugs"


class ArvRegimens(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "ARV Regimens"
        verbose_name_plural = "ARV Regimens"


class ClinicServices(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Clinic Services"
        verbose_name_plural = "Clinic Services"


class ClinicalWithdrawalReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Clinical Withdrawal Reasons"
        verbose_name_plural = "Clinical Withdrawal Reasons"


class Conditions(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Conditions"
        verbose_name_plural = "Conditions"


class DmManagement(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Diabetes Management"
        verbose_name_plural = "Diabetes Management"


class HtnManagement(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "HTN Management"
        verbose_name_plural = "HTN Management"


class DmTreatments(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Diabetes Treatments"
        verbose_name_plural = "Diabetes Treatments"


class DrugDispensaries(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Drug Dispensaries"
        verbose_name_plural = "Drug Dispensaries"


class DrugDispensers(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Drug Dispensers"
        verbose_name_plural = "Drug Dispensers"


class HealthAdvisors(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Health Advisors"
        verbose_name_plural = "Health Advisors"


class HealthInterventionTypes(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Health Intervention Types"
        verbose_name_plural = "Health Intervention Types"


class HealthServices(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Health Services"
        verbose_name_plural = "Health Services"


class HealthTalkTypes(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Health Talk Type"
        verbose_name_plural = "Health Talk Types"


class HealthTalkConditions(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Health Talk Conditions"
        verbose_name_plural = "Health Talk Conditions"


class HtnTreatments(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Hypertension Treatments"
        verbose_name_plural = "Hypertension Treatments"


class LaboratoryTests(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Laboratory Tests"
        verbose_name_plural = "Laboratory Tests"


class OffstudyReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Offstudy Reasons"
        verbose_name_plural = "Offstudy Reasons"


class NonAdherenceReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "NonAdherence Reasons"
        verbose_name_plural = "NonAdherence Reasons"


class RefillConditions(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Refill Conditions"
        verbose_name_plural = "Refill Conditions"


class ToxicityWithdrawalReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Toxicity Withdrawal Reasons"
        verbose_name_plural = "Toxicity Withdrawal Reasons"


class VisitReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Visit Reasons"
        verbose_name_plural = "Visit Reasons"


class SubjectVisitMissedReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Subject Missed Visit Reasons"
        verbose_name_plural = "Subject Missed Visit Reasons"


class DrugPaySources(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Drug Payment Sources"
        verbose_name_plural = "Drug Payment Sources"


class TransferReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Transfer Reasons"
        verbose_name_plural = "Transfer Reasons"


class TransportChoices(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Transport Choices"
        verbose_name_plural = "Transport Choices"


class HealthFacilityTypes(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Health Facility Type"
        verbose_name_plural = "Health Facility Types"


class LocationTypes(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Community-care location type"
        verbose_name_plural = "Community-care location types"


class RxModificationReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Treatment Modification Reasons"
        verbose_name_plural = "Treatment Modification Reasons"


class RxModifications(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Treatment Modifications"
        verbose_name_plural = "Treatment Modifications"


class ScreeningRefusalReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Screening Refusal Reasons"
        verbose_name_plural = "Screening Refusal Reasons"


class ConsentRefusalReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Consent Refusal Reasons"
        verbose_name_plural = "Consent Refusal Reasons"
