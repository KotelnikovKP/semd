from django.db import models
from django.db.models import Index

from backend.models.patient_models import Patient


class SEMD(models.Model):
    # SEMD
    internal_message_id = models.CharField(max_length=36, primary_key=True,
                                           verbose_name='Structured Electronic Medical Document identifier')
    document_type = models.CharField(max_length=8, verbose_name='Structured Electronic Medical Document type')
    sms_profile = models.CharField(max_length=10, verbose_name='Structured Electronic Medical Document profile')
    date_time_create = models.DateTimeField(verbose_name='Date time create')
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='semd',
                                null=True, blank=True, verbose_name='Patient')
    mo = models.CharField(blank=True, max_length=35, null=True, verbose_name='Medical organization code')
    medical_organization = models.ForeignKey('MedicalOrganization', on_delete=models.PROTECT, related_name='semd',
                                             null=True, blank=True, verbose_name='Medical organization')
    doctor = models.CharField(max_length=255, null=True, blank=True, verbose_name='Doctor name')
    doctor_job_title = models.CharField(max_length=255, null=True, blank=True, verbose_name='Doctor job title')
    medical_position = models.ForeignKey('MedicalPosition', on_delete=models.PROTECT, related_name='semd',
                                         null=True, blank=True, verbose_name='Medical position')
    diagnoses = models.CharField(max_length=150, null=True, blank=True, verbose_name='Diagnosis code')
    service = models.CharField(blank=True, max_length=25, null=True, verbose_name='Medical service code')
    medical_service = models.ForeignKey('MedicalService', on_delete=models.PROTECT, related_name='semd',
                                        null=True, blank=True, verbose_name='Medical service')
    service_time_str = models.CharField(max_length=20, verbose_name='Medical service date time')
    service_time = models.DateTimeField(null=True, blank=True, verbose_name='Medical service date time')

    # SEMD 2, 4
    res_protocol = models.CharField(null=True, blank=True, verbose_name='Result protocol')
    res_conclusion = models.CharField(null=True, blank=True, verbose_name='Result conclusion')
    res_recommendation = models.CharField(null=True, blank=True, verbose_name='Result recommendation')
    condition = models.CharField(max_length=25, null=True, blank=True, verbose_name='Condition')
    patient_condition = models.CharField(null=True, blank=True, verbose_name='Doctor visit patient condition')
    diagnosis = models.CharField(null=True, blank=True, verbose_name='Doctor visit diagnosis')

    # SEMD 3
    test_code = models.CharField(null=True, blank=True, verbose_name='Tests codes')
    test_value = models.CharField(null=True, blank=True, verbose_name='Tests values')
    test_unit = models.CharField(null=True, blank=True, verbose_name='Tests units')

    # SEMD 5
    patient_in_condition = models.CharField(null=True, blank=True, verbose_name='Hospital patient in condition')
    patient_out_condition = models.CharField(null=True, blank=True, verbose_name='Hospital patient out condition')
    start_date_str = models.CharField(null=True, blank=True, verbose_name='Hospital start date str')
    start_date = models.DateField(null=True, blank=True, verbose_name='Hospital start date')
    end_date_str = models.CharField(null=True, blank=True, verbose_name='Hospital end date str')
    end_date = models.DateField(null=True, blank=True, verbose_name='Hospital end date')
    hospitalization_urgency = models.CharField(null=True, blank=True, verbose_name='Hospital urgency')
    hospitalization_results = models.CharField(null=True, blank=True, verbose_name='Hospital results')

    def __str__(self):
        return self.internal_message_id

    class Meta:
        verbose_name = 'SEMD'
        verbose_name_plural = 'SEMD'
        ordering = ['date_time_create']
        indexes = (
            Index(fields=['date_time_create'], name='semd__date_time_create__idx'),
        )
