from rest_framework import serializers

from backend.models.ref_inf_models import MedicalService, Diagnosis, MedicalOrganization, LaboratoryTest
from backend.serializers.serializers import PaginationListSerializer, BaseResponseSerializer


class MedicalServiceSerializer(serializers.ModelSerializer):
    """
        Standard medical service schema (for all responses)
    """
    class Meta:
        model = MedicalService
        fields = ('ms_code', 'name', 'rel', 'dateout', )


class MedicalServiceListSerializer(BaseResponseSerializer):
    """
        Medical service list schema
    """
    result = MedicalServiceSerializer(many=True)
    retExtInfo = PaginationListSerializer()


class DiagnosisSerializer(serializers.ModelSerializer):
    """
        Standard diagnosis schema (for all responses)
    """
    class Meta:
        model = Diagnosis
        fields = ('mkb_code', 'name', 'rel', 'dateout', 'rec_code', 'id', 'id_parent', 'add_code')


class DiagnosisListSerializer(BaseResponseSerializer):
    """
        Diagnosis list schema
    """
    result = DiagnosisSerializer(many=True)
    retExtInfo = PaginationListSerializer()


class MedicalOrganizationSerializer(serializers.ModelSerializer):
    """
        Standard Medical organization schema (for all responses)
    """
    class Meta:
        model = MedicalOrganization
        fields = ('oid', 'nameFull', 'nameShort', 'medicalSubjectId', 'medicalSubjectName', 'inn',
                  'kpp', 'ogrn', 'regionId', 'regionName', 'moAgencyKind', 'id')


class MedicalOrganizationListSerializer(BaseResponseSerializer):
    """
        Medical organization list schema
    """
    result = MedicalOrganizationSerializer(many=True)
    retExtInfo = PaginationListSerializer()


class LaboratoryTestSerializer(serializers.ModelSerializer):
    """
        Standard laboratory test schema (for all responses)
    """
    class Meta:
        model = LaboratoryTest
        fields = ('id', 'name', 'eng_name', 'short_name', 'group_tests', 'mkb10_codes')


class LaboratoryTestListSerializer(BaseResponseSerializer):
    """
        Laboratory test list schema
    """
    result = LaboratoryTestSerializer(many=True)
    retExtInfo = PaginationListSerializer()


