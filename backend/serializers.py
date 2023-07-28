from django.contrib.auth.models import User
from rest_framework import serializers, status

from backend.models import MedicalService, Diagnosis, MedicalOrganization, LaboratoryTest, Patient, PatientDiagnosis


class SimpleResponseSerializer(serializers.Serializer):
    """
        Error schema
    """
    detail = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


simple_responses = {
    status.HTTP_400_BAD_REQUEST: SimpleResponseSerializer,
    status.HTTP_401_UNAUTHORIZED: SimpleResponseSerializer,
    status.HTTP_403_FORBIDDEN: SimpleResponseSerializer,
    status.HTTP_404_NOT_FOUND: SimpleResponseSerializer,
}


class BaseResponseSerializer(serializers.Serializer):
    """
        Base response schema (all response schema are its children)
    """
    retCode = serializers.IntegerField(help_text='Return code')
    retMsg = serializers.CharField(help_text='Return message')
    result = serializers.CharField(help_text='Result')
    retExtInfo = serializers.CharField(help_text='External result information')
    retTime = serializers.IntegerField(help_text='Return timestamp')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class PaginationListSerializer(serializers.Serializer):
    """
        Pagination list's extra information schema
    """
    count_items = serializers.IntegerField(help_text='Total number of items in result set')
    items_per_page = serializers.IntegerField(help_text='Number of items on one page')
    start_item_index = serializers.IntegerField(help_text='Index of start item on current page')
    end_item_index = serializers.IntegerField(help_text='Index of end item on current page')
    previous_page = serializers.IntegerField(help_text='Number of previous page (null if the current page is the last)')
    current_page = serializers.IntegerField(help_text='Number of current page')
    next_page = serializers.IntegerField(help_text='Number of next page (null if the current page is the first)')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):
    """
        Standard user schema (for all responses)
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', )


class UserRegisterSerializer(serializers.ModelSerializer):
    """
        User registration schema

        1. Fields validation
        2. Check equalization of passwords
    """
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "password2", )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords aren't equal"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserCreateSerializer(BaseResponseSerializer):
    """
        User create response schema
    """
    result = UserSerializer(many=False)


class UserDetailsSerializer(serializers.Serializer):
    """
        User retrieve schema
    """
    user = UserSerializer(many=False)


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


class PatientSerializer(serializers.ModelSerializer):
    """
        Standard patient schema (for all responses)
    """
    class Meta:
        model = Patient
        fields = ('snils', 'name', 'gender', 'birthday')


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


class PatientDiagnosisSerializer(serializers.ModelSerializer):
    """
        Standard patient diagnosis schema (for all responses)
    """
    class Meta:
        model = PatientDiagnosis
        fields = ('id', 'patient_id', 'diagnosis_id')


class PatientDiagnosisListSerializer(BaseResponseSerializer):
    """
        Patient diagnosis list schema
    """
    result = PatientDiagnosisSerializer(many=True)
    retExtInfo = PaginationListSerializer()


