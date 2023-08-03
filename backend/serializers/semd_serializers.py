from rest_framework import serializers

from backend.models.semd_models import SEMD, SemdTest
from backend.serializers.serializers import BaseResponseSerializer, PaginationListSerializer


class SEMDSerializer(serializers.ModelSerializer):
    """
        Standard SEMD schema (for all responses)
    """
    patient_name = serializers.SerializerMethodField(help_text='Patient FIO')
    patient_gender = serializers.SerializerMethodField(help_text='Patient gender')
    patient_birthday = serializers.SerializerMethodField(help_text='Patient birthday')
    medical_organization_name = serializers.SerializerMethodField(help_text='Medical organization')
    medical_position_name = serializers.SerializerMethodField(help_text='Doctor position')
    medical_service_name = serializers.SerializerMethodField(help_text='Medical service')
    patient_diagnosis_name = serializers.SerializerMethodField(help_text='Patient diagnosis in doctor visit')

    class Meta:
        model = SEMD
        fields = ('internal_message_id', 'document_type', 'sms_profile', 'date_time_create',
                  'patient_id', 'patient_name', 'patient_gender', 'patient_birthday',
                  'medical_organization_id', 'medical_organization_name',
                  'doctor', 'medical_position_id', 'medical_position_name',
                  'diagnoses', 'medical_service_id', 'medical_service_name', 'service_time',
                  'place_of_service', 'res_protocol', 'res_conclusion', 'res_recommendation',
                  'patient_condition', 'patient_diagnosis_id', 'patient_diagnosis_name',
                  'patient_in_condition', 'patient_out_condition', 'start_date', 'end_date',
                  'hospitalization_results', 'hospitalization_urgency')

    @staticmethod
    def get_patient_name(obj) -> serializers.CharField:
        return obj.patient.name if isinstance(obj, SEMD) else dict(obj)['patient'].name

    @staticmethod
    def get_patient_gender(obj) -> serializers.CharField:
        return obj.patient.gender if isinstance(obj, SEMD) else dict(obj)['patient'].gender

    @staticmethod
    def get_patient_birthday(obj) -> serializers.CharField:
        return obj.patient.birthday if isinstance(obj, SEMD) else dict(obj)['patient'].birthday

    @staticmethod
    def get_medical_organization_name(obj) -> serializers.CharField:
        return obj.medical_organization.nameFull if isinstance(obj, SEMD) else dict(obj)['medical_organization'].nameFull

    @staticmethod
    def get_medical_position_name(obj) -> serializers.CharField:
        return obj.medical_position.name if isinstance(obj, SEMD) else dict(obj)['medical_position'].name

    @staticmethod
    def get_medical_service_name(obj) -> serializers.CharField:
        medical_service = obj.medical_service if isinstance(obj, SEMD) else dict(obj).get('medical_service', None)
        return None if medical_service is None else medical_service.name

    @staticmethod
    def get_patient_diagnosis_name(obj) -> serializers.CharField:
        patient_diagnosis = obj.patient_diagnosis if isinstance(obj, SEMD) else dict(obj).get('patient_diagnosis', None)
        return None if patient_diagnosis is None else patient_diagnosis.name


class SEMDListSerializer(BaseResponseSerializer):
    """
        SEMD list schema
    """
    result = SEMDSerializer(many=True)
    retExtInfo = PaginationListSerializer()


class SEMDDetailsSerializer(BaseResponseSerializer):
    """
        SEMD details schema
    """
    result = SEMDSerializer(many=False)


class SemdTestSerializer(serializers.ModelSerializer):
    """
        Standard SEMD test schema (for all responses)
    """
    patient_name = serializers.SerializerMethodField(help_text='Patient FIO')
    patient_gender = serializers.SerializerMethodField(help_text='Patient gender')
    patient_birthday = serializers.SerializerMethodField(help_text='Patient birthday')
    laboratory_test_name = serializers.SerializerMethodField(help_text='Laboratory test name')

    class Meta:
        model = SemdTest
        fields = ('id', 'semd_id', 'test_time', 'patient_id', 'patient_name', 'patient_gender', 'patient_birthday',
                  'laboratory_test_id', 'laboratory_test_name', 'value')

    @staticmethod
    def get_patient_name(obj) -> serializers.CharField:
        return obj.patient.name if isinstance(obj, SemdTest) else dict(obj)['patient_name']

    @staticmethod
    def get_patient_gender(obj) -> serializers.CharField:
        return obj.patient.gender if isinstance(obj, SemdTest) else dict(obj)['patient_gender']

    @staticmethod
    def get_patient_birthday(obj) -> serializers.CharField:
        return obj.patient.birthday if isinstance(obj, SemdTest) else dict(obj)['patient_birthday']

    @staticmethod
    def get_laboratory_test_name(obj) -> serializers.CharField:
        # laboratory_test = obj.laboratory_test if isinstance(obj, SemdTest) else dict(obj).get('laboratory_test', None)
        # return None if laboratory_test is None else laboratory_test.name
        return obj.laboratory_test.name if isinstance(obj, SemdTest) else dict(obj)['laboratory_test_name']


class SemdTestListSerializer(BaseResponseSerializer):
    """
        SEMD test list schema
    """
    result = SemdTestSerializer(many=True)
    retExtInfo = PaginationListSerializer()


class SemdTestDetailsSerializer(BaseResponseSerializer):
    """
        SEMD test details schema
    """
    result = SemdTestSerializer(many=False)


