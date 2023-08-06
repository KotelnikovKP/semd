from rest_framework import serializers

from backend.models.registry_models import DiagnosisRegistry, DiagnosisRegistryItem
from backend.serializers.serializers import BaseResponseSerializer, PaginationListSerializer


class DiagnosisRegistrySerializer(serializers.ModelSerializer):
    """
        Standard diagnosis registry schema
    """
    # medical_record_transcript_settings = \
    #     serializers.SerializerMethodField(help_text='Settings of medical record transcript')
    #
    class Meta:
        model = DiagnosisRegistry
        fields = ('id', 'name', 'short_name', 'medical_record_transcript_settings')
        read_only_fields = ('id', )
    #
    # @staticmethod
    # def get_medical_record_transcript_settings(obj) -> serializers.JSONField:
    #     return obj.medical_record_transcript_settings


class DiagnosisRegistryListSerializer(BaseResponseSerializer):
    """
        Diagnosis registry list response schema
    """
    result = DiagnosisRegistrySerializer(many=True)
    retExtInfo = PaginationListSerializer()


class DiagnosisRegistrySingleEntrySerializer(BaseResponseSerializer):
    """
        Diagnosis registry single entry response schema
    """
    result = DiagnosisRegistrySerializer(many=False)


class DiagnosisRegistryItemSerializer(serializers.ModelSerializer):
    """
        Standard diagnosis registry item schema
    """
    registry_name = serializers.SerializerMethodField(help_text='Name of registry')
    diagnosis_name = serializers.SerializerMethodField(help_text='Name of diagnosis')

    class Meta:
        model = DiagnosisRegistryItem
        fields = ('id', 'registry', 'registry_name', 'diagnosis', 'diagnosis_name')
        read_only_fields = ('id', 'registry_name', 'diagnosis_name')

    @staticmethod
    def get_registry_name(obj) -> serializers.CharField:
        return obj.registry.short_name if isinstance(obj, DiagnosisRegistryItem) else dict(obj)['registry'].short_name

    @staticmethod
    def get_diagnosis_name(obj) -> serializers.CharField:
        return obj.diagnosis.name if isinstance(obj, DiagnosisRegistryItem) else dict(obj)['diagnosis'].name


class DiagnosisRegistryItemListSerializer(BaseResponseSerializer):
    """
        Diagnosis registry item list schema
    """
    result = DiagnosisRegistryItemSerializer(many=True)
    retExtInfo = PaginationListSerializer()


class DiagnosisRegistryItemSingleEntrySerializer(BaseResponseSerializer):
    """
        Diagnosis registry item single entry response schema
    """
    result = DiagnosisRegistryItemSerializer(many=False)
