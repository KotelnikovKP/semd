from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from backend.filters import MedicalServiceFilter, DiagnosisFilter, MedicalOrganizationFilter, LaboratoryTestFilter, \
    PatientFilter
from backend.helpers import expand_dict
from backend.models import MedicalService, Diagnosis, MedicalOrganization, LaboratoryTest, Patient
from backend.permissions import OnlyListPermission, ListRetrievePermission, PatientPermission
# from backend.permissions import SemdPermission
from backend.serializers import simple_responses, UserRegisterSerializer, UserCreateSerializer, UserDetailsSerializer, \
    MedicalServiceSerializer, MedicalServiceListSerializer, DiagnosisSerializer, DiagnosisListSerializer, \
    MedicalOrganizationSerializer, MedicalOrganizationListSerializer, LaboratoryTestSerializer, \
    LaboratoryTestListSerializer, PatientSerializer, PatientListSerializer, PatientDetailsSerializer, \
    PatientDiagnosisListSerializer
from backend.services import CreateUserService, GetUserDetailsService, GetMedicalServiceListService, \
    GetDiagnosisListService, GetMedicalOrganizationListService, GetLaboratoryTestListService, GetPatientListService, \
    GetPatientDetailsService, GetPatientDiagnosesService


@extend_schema(tags=['Auth'])
@extend_schema_view(
    post=extend_schema(
        summary='Authorize user and retrieve an access token',
        description='Authorize user and retrieve a bearer token, bla-bla-bla...',
    ),
)
class SemdCustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=['Auth'])
@extend_schema_view(
    post=extend_schema(
        summary='Refresh token',
        description='Refresh token, bla-bla-bla...',
    ),
)
class SemdCustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=['Auth'])
class UserRegisterViewSet(ModelViewSet):
    permission_classes = (AllowAny, )
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    @extend_schema(
        summary='Register user',
        description='Register user, bla-bla-bla...',
        request=UserRegisterSerializer(many=False),
        responses=expand_dict({status.HTTP_200_OK: UserCreateSerializer, }, simple_responses),
    )
    def create(self, request, *args, **kwargs):
        """
            User registration
        """
        user_create = CreateUserService.execute(request, self, *args, **kwargs)
        return Response(user_create.data)

    @extend_schema(
        summary='Retrieve user profile',
        description='Retrieve user profile, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: UserDetailsSerializer, }, simple_responses),
    )
    def retrieve(self, request, *args, **kwargs):
        """
            Retrieve user profile
        """
        user_details = GetUserDetailsService.execute(request, self, *args, **kwargs)
        return Response({"user": user_details.data})


@extend_schema(tags=['Medical Service'])
class MedicalServiceViewSet(ModelViewSet):

    permission_classes = (OnlyListPermission, )
    queryset = MedicalService.objects.all()
    serializer_class = MedicalServiceSerializer
    filterset_class = MedicalServiceFilter

    @extend_schema(
        summary='Retrieve paginated and filtered list of medical services',
        description='Retrieve paginated and filtered list of medical services, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: MedicalServiceListSerializer, }, simple_responses),
    )
    def list(self, request: Request, *args, **kwargs):
        """
            Retrieve list of medical services
        """
        medical_service_list = GetMedicalServiceListService.execute(request, self, *args, **kwargs)
        return Response(medical_service_list.data)


@extend_schema(tags=['Diagnosis'])
class DiagnosisViewSet(ModelViewSet):

    permission_classes = (OnlyListPermission, )
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
    filterset_class = DiagnosisFilter

    @extend_schema(
        summary='Retrieve paginated and filtered list of diagnoses',
        description='Retrieve paginated and filtered list of diagnoses, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: DiagnosisListSerializer, }, simple_responses),
    )
    def list(self, request: Request, *args, **kwargs):
        """
            Retrieve list of diagnoses
        """
        diagnosis_list = GetDiagnosisListService.execute(request, self, *args, **kwargs)
        return Response(diagnosis_list.data)


@extend_schema(tags=['Medical Organization'])
class MedicalOrganizationViewSet(ModelViewSet):

    permission_classes = (OnlyListPermission, )
    queryset = MedicalOrganization.objects.all()
    serializer_class = MedicalOrganizationSerializer
    filterset_class = MedicalOrganizationFilter

    @extend_schema(
        summary='Retrieve paginated and filtered list of medical organizations',
        description='Retrieve paginated and filtered list of medical organizations, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: MedicalOrganizationListSerializer, }, simple_responses),
    )
    def list(self, request: Request, *args, **kwargs):
        """
            Retrieve list of medical organizations
        """
        medical_organization_list = GetMedicalOrganizationListService.execute(request, self, *args, **kwargs)
        return Response(medical_organization_list.data)


@extend_schema(tags=['Laboratory test'])
class LaboratoryTestViewSet(ModelViewSet):

    permission_classes = (OnlyListPermission, )
    queryset = LaboratoryTest.objects.all()
    serializer_class = LaboratoryTestSerializer
    filterset_class = LaboratoryTestFilter

    @extend_schema(
        summary='Retrieve paginated and filtered list of laboratory tests',
        description='Retrieve paginated and filtered list of laboratory tests, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: LaboratoryTestListSerializer, }, simple_responses),
    )
    def list(self, request: Request, *args, **kwargs):
        """
            Retrieve list of laboratory tests
        """
        laboratory_test_list = GetLaboratoryTestListService.execute(request, self, *args, **kwargs)
        return Response(laboratory_test_list.data)


@extend_schema(tags=['Patient'])
class PatientViewSet(ModelViewSet):

    permission_classes = (PatientPermission, )
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filterset_class = PatientFilter

    @extend_schema(
        summary='Retrieve paginated and filtered list of patients',
        description='Retrieve paginated and filtered list of patients, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: PatientListSerializer, }, simple_responses),
    )
    def list(self, request: Request, *args, **kwargs):
        """
            Retrieve list of patients
        """
        patient_list = GetPatientListService.execute(request, self, *args, **kwargs)
        return Response(patient_list.data)

    @extend_schema(
        summary='Retrieve detail of patient',
        description='Retrieve detail of patient, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: PatientDetailsSerializer, }, simple_responses),
    )
    def retrieve(self, request, *args, **kwargs):
        """
            Retrieve detail of patient
        """
        patient_details = GetPatientDetailsService.execute(request, self, *args, **kwargs)
        return Response(patient_details.data)

    @extend_schema(
        summary='Retrieve diagnoses of patient',
        description='Retrieve diagnoses of patient, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: PatientDiagnosisListSerializer, }, simple_responses),
    )
    @action(detail=True)
    def diagnoses(self, request, *args, **kwargs):
        """
            Retrieve diagnoses of patient
        """
        patient_diagnoses = GetPatientDiagnosesService.execute(request, self, *args, **kwargs)
        return Response(patient_diagnoses.data)
