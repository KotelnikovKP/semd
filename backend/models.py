from django.db import models
from django.db.models import Index, UniqueConstraint


class MedicalService(models.Model):
    ms_code = models.CharField(max_length=25, primary_key=True, verbose_name='Medical service code')
    name = models.CharField(max_length=500, verbose_name='Medical service name')
    rel = models.IntegerField(verbose_name='Sign of relevance')
    dateout = models.DateField(null=True, blank=True, verbose_name='Date out')

    def __str__(self):
        return str(self.ms_code) + ' ' + str(self.name)

    class Meta:
        verbose_name = 'Medical service'
        verbose_name_plural = 'Medical services'
        ordering = ['ms_code']
        indexes = (
            Index(fields=['name'], name='med_ser__name__idx'),
        )


class Diagnosis(models.Model):
    mkb_code = models.CharField(max_length=15, primary_key=True, verbose_name='Diagnosis code (MKB-10)')
    rec_code = models.CharField(max_length=15, verbose_name='Sorted code')
    id = models.IntegerField(verbose_name='Identifier')
    id_parent = models.IntegerField(null=True, blank=True, verbose_name='Parent identifier')
    name = models.CharField(max_length=300, verbose_name='Diagnosis name')
    add_code = models.IntegerField(null=True, blank=True, verbose_name='Addition code')
    rel = models.IntegerField(verbose_name='Sign of relevance')
    dateout = models.DateField(null=True, blank=True, verbose_name='Date out')

    def __str__(self):
        return str(self.mkb_code) + ' ' + str(self.name)

    class Meta:
        verbose_name = 'Diagnosis'
        verbose_name_plural = 'Diagnoses'
        ordering = ['rec_code']
        indexes = (
            Index(fields=['rec_code'], name='dia__rec_code__idx'),
            Index(fields=['name'], name='dia__name__idx'),
            Index(fields=['id'], name='dia__id__idx'),
            Index(fields=['id_parent'], name='dia__id_parent__idx'),
        )


class MedicalOrganization(models.Model):
    oid = models.CharField(max_length=35, primary_key=True, verbose_name='Medical organization code')
    id = models.IntegerField(verbose_name='Identifier')
    nameFull = models.CharField(max_length=400, verbose_name='Medical organization full name')
    nameShort = models.CharField(max_length=350, null=True, blank=True, verbose_name='Medical organization short name')
    medicalSubjectId = models.IntegerField(null=True, blank=True, verbose_name='Medical subject code')
    medicalSubjectName = models.CharField(max_length=140, null=True, blank=True, verbose_name='Medical subject name')
    inn = models.CharField(max_length=12, null=True, blank=True, verbose_name='INN')
    kpp = models.CharField(max_length=9, null=True, blank=True, verbose_name='KPP')
    ogrn = models.CharField(max_length=15, null=True, blank=True, verbose_name='OGRN')
    regionId = models.IntegerField(null=True, blank=True, verbose_name='Region code')
    regionName = models.CharField(max_length=50, null=True, blank=True, verbose_name='Region name')
    moAgencyKind = models.CharField(max_length=70, null=True, blank=True, verbose_name='Agency kind')

    def __str__(self):
        return str(self.oid) + ' ' + str(self.nameShort)

    class Meta:
        verbose_name = 'Medical organization'
        verbose_name_plural = 'Medical organizations'
        ordering = ['oid']
        indexes = (
            Index(fields=['nameShort'], name='med_org__name__idx'),
            Index(fields=['id'], name='med_org__id__idx'),
        )


class LaboratoryTest(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='Laboratory test code')
    name = models.CharField(max_length=300, verbose_name='Laboratory test name')
    eng_name = models.CharField(max_length=300, null=True, blank=True, verbose_name='Laboratory test english name')
    short_name = models.CharField(max_length=250, null=True, blank=True, verbose_name='Laboratory test short name')
    group_tests = models.CharField(max_length=100, null=True, blank=True, verbose_name='Group tests name')
    mkb10_codes = models.CharField(max_length=300, null=True, blank=True, verbose_name='Medical service codes')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Laboratory test'
        verbose_name_plural = 'Laboratory tests'
        ordering = ['id']
        indexes = (
            Index(fields=['name'], name='lab_tes__name__idx'),
        )


class Patient(models.Model):
    snils = models.CharField(max_length=11, primary_key=True, verbose_name='Patient SNILS')
    name = models.CharField(max_length=255, verbose_name='Patient name')
    gender = models.CharField(max_length=7, null=True, blank=True, verbose_name='Patient gender')
    birthday = models.DateField(null=True, blank=True, verbose_name='Patient birthday')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['name']
        indexes = (
            Index(fields=['name'], name='pat__name__idx'),
        )


class PatientDiagnosis(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT, related_name='diagnoses',
                                null=True, blank=True, verbose_name='patient')
    diagnosis = models.ForeignKey('Diagnosis', on_delete=models.PROTECT, related_name='patients',
                                  null=True, blank=True, verbose_name='diagnosis')

    def __str__(self):
        return str(self.patient_id) + ' ' + str(self.diagnosis_id)

    class Meta:
        verbose_name = 'Patient diagnosis'
        verbose_name_plural = 'Patients diagnoses'
        ordering = ['patient_id']
        indexes = (
            Index(fields=['diagnosis_id'], name='pat_dia__diagnosis__idx'),
        )
        constraints = (
            UniqueConstraint(fields=['patient_id', 'diagnosis_id'], name='pat_dia__snils_dia__unq'),
        )


class PatientMedicalCard(models.Model):
    card_type = models.CharField(max_length=3, verbose_name='Medical card type')
    card_number = models.CharField(max_length=40, verbose_name='Medical card number')
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT, related_name='medical_cards',
                                null=True, blank=True, verbose_name='patient')

    def __str__(self):
        return str(self.patient_id) + ' ' + str(self.card_type) + ' ' + str(self.card_number)

    class Meta:
        verbose_name = 'Patient medical card'
        verbose_name_plural = 'Patients medical cards'
        ordering = ['patient_id']
        indexes = (
            Index(fields=['card_number'], name='pat_car__card_number__idx'),
        )
        constraints = (
            UniqueConstraint(fields=['patient_id', 'card_type', 'card_number'], name='pat_car__snils_t_n__unq'),
        )


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


