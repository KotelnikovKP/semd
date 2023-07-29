from django.db import models
from django.db.models import Index


class SEMD2(models.Model):
    internal_message_id = models.CharField(max_length=36, primary_key=True,
                                           verbose_name='Structured Electronic Medical Document identifier')
    sms_profile = models.CharField(max_length=10, verbose_name='Structured Electronic Medical Document profile')
    date_time_create = models.DateTimeField(verbose_name='Date time create')
    patient_snils = models.CharField(max_length=11, verbose_name='Patient SNILS')
    patient = models.CharField(max_length=255, verbose_name='Patient name')
    patient_gender = models.CharField(max_length=7, verbose_name='Patient gender')
    patient_birthday_str = models.CharField(max_length=8, verbose_name='Patient birthday')
    doctor = models.CharField(max_length=255, null=True, blank=True, verbose_name='Doctor name')
    doctor_job_title = models.CharField(max_length=255, null=True, blank=True, verbose_name='Doctor job title')
    diagnoses = models.CharField(max_length=150, null=True, blank=True, verbose_name='Diagnosis code')
    service_time = models.DateTimeField(null=True, blank=True, verbose_name='Medical service date time')
    service_time_str = models.CharField(max_length=20, verbose_name='Medical service date time')
    res_protocol = models.CharField(null=True, blank=True, verbose_name='Result protocol')
    res_conclusion = models.CharField(null=True, blank=True, verbose_name='Result conclusion')
    res_recommendation = models.CharField(null=True, blank=True, verbose_name='Result recommendation')
    condition = models.CharField(max_length=25, null=True, blank=True, verbose_name='Condition')
    med_card_amb = models.CharField(max_length=50, null=True, blank=True, verbose_name='Ambulatory medical file')
    med_card_sta = models.CharField(max_length=50, null=True, blank=True, verbose_name='Stationary medical file')
    medical_organization = models.ForeignKey('MedicalOrganization', on_delete=models.PROTECT, related_name='semd2',
                                             null=True, blank=True, verbose_name='Medical organization')
    medical_service = models.ForeignKey('MedicalService', on_delete=models.PROTECT, related_name='semd2',
                                        null=True, blank=True, verbose_name='Medical service')

    def __str__(self):
        return self.internal_message_id

    class Meta:
        verbose_name = 'SEMD 2'
        verbose_name_plural = 'SEMD 2'
        ordering = ['date_time_create']
        indexes = (
            Index(fields=['date_time_create'], name='semd2__date_time_create__idx'),
        )


