from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from backend.filters.ref_inf_filters import MedicalServiceFilter, DiagnosisFilter, MedicalOrganizationFilter, \
    LaboratoryTestFilter
from backend.helpers import expand_dict
from backend.models.ref_inf_models import MedicalService, Diagnosis, MedicalOrganization, LaboratoryTest
from backend.permissions.permissions import OnlyListPermission
from backend.serializers.ref_inf_serializers import MedicalServiceSerializer, MedicalServiceListSerializer, \
    DiagnosisSerializer, DiagnosisListSerializer, MedicalOrganizationSerializer, MedicalOrganizationListSerializer, \
    LaboratoryTestSerializer, LaboratoryTestListSerializer
from backend.serializers.serializers import simple_responses
from backend.services.ref_Inf_services import GetMedicalServiceListService, GetDiagnosisListService, \
    GetMedicalOrganizationListService, GetLaboratoryTestListService


@extend_schema(tags=['Reference Information'])
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


@extend_schema(tags=['Reference Information'])
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


@extend_schema(tags=['Reference Information'])
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


@extend_schema(tags=['Reference Information'])
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
