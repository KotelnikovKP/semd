from rest_framework import serializers

from backend.models.registry_models import DiagnosisRegistry, DiagnosisRegistryItem
from backend.serializers.serializers import BaseResponseSerializer, PaginationListSerializer


class DiagnosisRegistrySerializer(serializers.ModelSerializer):
    """
        Standard diagnosis registry schema (for all responses)
    """
    class Meta:
        model = DiagnosisRegistry
        fields = ('id', 'name', 'short_name')


class DiagnosisRegistryListSerializer(BaseResponseSerializer):
    """
        Diagnosis registry list schema
    """
    result = DiagnosisRegistrySerializer(many=True)
    retExtInfo = PaginationListSerializer()


class DiagnosisRegistryItemSerializer(serializers.ModelSerializer):
    """
        Standard diagnosis registry item schema (for all responses)
    """
    diagnosis_name = serializers.SerializerMethodField(help_text='Name of diagnosis')

    class Meta:
        model = DiagnosisRegistryItem
        fields = ('id', 'registry_id', 'diagnosis_id', 'diagnosis_name')

    @staticmethod
    def get_diagnosis_name(obj) -> serializers.CharField:
        return obj.diagnosis.name if isinstance(obj, DiagnosisRegistryItem) else dict(obj)['diagnosis'].name


class DiagnosisRegistryItemListSerializer(BaseResponseSerializer):
    """
        Diagnosis registry item list schema
    """
    result = DiagnosisRegistryItemSerializer(many=True)
    retExtInfo = PaginationListSerializer()
