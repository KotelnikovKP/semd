from rest_framework import serializers

from backend.models.patient_models import Patient, PatientDiagnosis, PatientMedicalCard
from backend.serializers.semd_serializers import SEMDSerializer, SemdTestSerializer
from backend.serializers.serializers import BaseResponseSerializer, PaginationListSerializer


class PatientDiagnosisSerializer(serializers.ModelSerializer):
    """
        Standard patient diagnosis schema (for all responses)
    """
    diagnosis_name = serializers.SerializerMethodField(help_text='Name of diagnosis')

    class Meta:
        model = PatientDiagnosis
        fields = ('id', 'patient_id', 'diagnosis_id', 'diagnosis_name')

    @staticmethod
    def get_diagnosis_name(obj) -> serializers.CharField:
        return obj.diagnosis.name if isinstance(obj, PatientDiagnosis) else dict(obj)['diagnosis'].name


class PatientDiagnosisListSerializer(BaseResponseSerializer):
    """
        Patient diagnosis list schema
    """
    result = PatientDiagnosisSerializer(many=True)
    retExtInfo = PaginationListSerializer()


class PatientMedicalCardSerializer(serializers.ModelSerializer):
    """
        Standard patient medical card schema (for all responses)
    """
    class Meta:
        model = PatientMedicalCard
        fields = ('id', 'patient_id', 'card_type', 'card_number')


class PatientMedicalCardListSerializer(BaseResponseSerializer):
    """
        Patient medical card list schema
    """
    result = PatientMedicalCardSerializer(many=True)
    retExtInfo = PaginationListSerializer()


class PatientSerializer(serializers.ModelSerializer):
    """
        Standard patient schema (for all responses)
    """
    diagnoses = PatientDiagnosisSerializer(many=True, read_only=True)
    medical_cards = PatientMedicalCardSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ('snils', 'name', 'gender', 'birthday', 'diagnoses', 'medical_cards')


class PatientListSerializer(BaseResponseSerializer):
    """
        Patient list schema
    """
    result = PatientSerializer(many=True)
    retExtInfo = PaginationListSerializer()


class PatientDetailsSerializer(BaseResponseSerializer):
    """
        Patient details schema
    """
    result = PatientSerializer(many=False)


class PatientRegistryReportSerializer(serializers.Serializer):
    """
        Patient Registry report schema
    """
    events = SEMDSerializer(many=True, read_only=True)
    medical_tests = SemdTestSerializer(many=True, read_only=True)
    medical_examinations = SEMDSerializer(many=True, read_only=True)
    treatment = SEMDSerializer(many=True, read_only=True)
    recommended_therapy = SEMDSerializer(many=True, read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class PatientRegistryReportDetailSerializer(BaseResponseSerializer):
    """
        Patient Registry report details schema
    """
    result = PatientRegistryReportSerializer()
