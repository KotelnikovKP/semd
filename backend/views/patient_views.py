from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from backend.filters.patient_filters import PatientFilter
from backend.helpers import expand_dict
from backend.models.patient_models import Patient
from backend.permissions.patient_permission import PatientPermission
from backend.serializers.patient_serializers import PatientSerializer, PatientListSerializer, \
    PatientDetailsSerializer, PatientDiagnosisListSerializer, PatientMedicalCardListSerializer, \
    PatientRegistryReportDetailSerializer
from backend.serializers.semd_serializers import SEMDListSerializer
from backend.serializers.serializers import simple_responses
from backend.services.patient_report_services import GetPatientRegistryReportService
from backend.services.patient_services import GetPatientListService, GetPatientDetailsService, \
    GetPatientDiagnosesService, GetPatientMedicalCardsService, GetPatientSemdsService, GetPatientSemdTestsService


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

    @extend_schema(
        summary='Retrieve medical cards of patient',
        description='Retrieve medical cards of patient, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: PatientMedicalCardListSerializer, }, simple_responses),
    )
    @action(detail=True)
    def medical_cards(self, request, *args, **kwargs):
        """
            Retrieve medical cards of patient
        """
        patient_medical_cards = GetPatientMedicalCardsService.execute(request, self, *args, **kwargs)
        return Response(patient_medical_cards.data)

    @extend_schema(
        summary='Retrieve SEMDs of patient',
        description='Retrieve SEMDs of patient, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: SEMDListSerializer, }, simple_responses),
    )
    @action(detail=True)
    def semds(self, request, *args, **kwargs):
        """
            Retrieve SEMD list of patient
        """
        patient_semds = GetPatientSemdsService.execute(request, self, *args, **kwargs)
        return Response(patient_semds.data)

    @extend_schema(
        summary='Retrieve laboratory tests of patient',
        description='Retrieve laboratory tests of patient, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: SEMDListSerializer, }, simple_responses),
    )
    @action(detail=True)
    def tests(self, request, *args, **kwargs):
        """
            Retrieve laboratory tests of patient
        """
        patient_semd_tests = GetPatientSemdTestsService.execute(request, self, *args, **kwargs)
        return Response(patient_semd_tests.data)

    @extend_schema(
        summary='Retrieve registry report of patient',
        description='Retrieve registry report of patient, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: PatientRegistryReportDetailSerializer, }, simple_responses),
    )
    @action(detail=True)
    def registry_report(self, request, *args, **kwargs):
        """
            Retrieve registry report of patient
        """
        patient_registry_report = GetPatientRegistryReportService.execute(request, self, *args, **kwargs)
        return Response(patient_registry_report.data)
