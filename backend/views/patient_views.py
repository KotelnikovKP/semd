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
    PatientDetailsSerializer, PatientDiagnosisListSerializer, PatientMedicalCardListSerializer
from backend.serializers.serializers import simple_responses
from backend.services.patient_services import GetPatientListService, GetPatientDetailsService, \
    GetPatientDiagnosesService, GetPatientMedicalCardsService


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
