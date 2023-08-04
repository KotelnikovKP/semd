from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from backend.filters.semd_filters import SEMDFilter, SemdTestFilter
from backend.helpers import expand_dict
from backend.models.semd_models import SEMD, SemdTest
from backend.permissions.permissions import ListRetrievePermission
from backend.permissions.semd_permission import SEMDPermission
from backend.serializers.semd_serializers import SEMDSerializer, SEMDListSerializer, \
    SEMDDetailsSerializer, SemdTestListSerializer, SemdTestSerializer, SemdTestDetailsSerializer
from backend.serializers.serializers import simple_responses
from backend.services.semd_services import GetSemdListService, GetSemdDetailsService, \
    GetSemdTestsService, GetSemdTestListService, GetSemdTestDetailsService


@extend_schema(tags=['SEMD'])
class SEMDViewSet(ModelViewSet):

    permission_classes = (SEMDPermission, )
    queryset = SEMD.objects.all().order_by('-date_time_create')
    serializer_class = SEMDSerializer
    filterset_class = SEMDFilter

    @extend_schema(
        summary='Retrieve paginated and filtered list of SEMDs',
        description='Retrieve paginated and filtered list of SEMDs, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: SEMDListSerializer, }, simple_responses),
    )
    def list(self, request: Request, *args, **kwargs):
        """
            Retrieve list of SEMDs
        """
        semd_list = GetSemdListService.execute(request, self, *args, **kwargs)
        return Response(semd_list.data)

    @extend_schema(
        summary='Retrieve detail of SEMD',
        description='Retrieve detail of SEMD, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: SEMDDetailsSerializer, }, simple_responses),
    )
    def retrieve(self, request, *args, **kwargs):
        """
            Retrieve detail of SEMD
        """
        semd_details = GetSemdDetailsService.execute(request, self, *args, **kwargs)
        return Response(semd_details.data)

    @extend_schema(
        summary='Retrieve tests of SEMD',
        description='Retrieve tests of SEMD, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: SemdTestListSerializer, }, simple_responses),
    )
    @action(detail=True)
    def tests(self, request, *args, **kwargs):
        """
            Retrieve tests of SEMD
        """
        semd_diagnoses = GetSemdTestsService.execute(request, self, *args, **kwargs)
        return Response(semd_diagnoses.data)


@extend_schema(tags=['SEMD'])
class SemdTestViewSet(ModelViewSet):

    permission_classes = (ListRetrievePermission, )
    queryset = SemdTest.objects.all().order_by('-test_time')
    serializer_class = SemdTestSerializer
    filterset_class = SemdTestFilter

    @extend_schema(
        summary='Retrieve paginated and filtered list of SEMD tests',
        description='Retrieve paginated and filtered list of SEMD tests, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: SemdTestListSerializer, }, simple_responses),
    )
    def list(self, request: Request, *args, **kwargs):
        """
            Retrieve list of SemdTests
        """
        semd_test_list = GetSemdTestListService.execute(request, self, *args, **kwargs)
        return Response(semd_test_list.initial_data)

    @extend_schema(
        summary='Retrieve detail of SEMD test',
        description='Retrieve detail of SEMD test, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: SemdTestDetailsSerializer, }, simple_responses),
    )
    def retrieve(self, request, *args, **kwargs):
        """
            Retrieve detail of SEMD test
        """
        semd_test_details = GetSemdTestDetailsService.execute(request, self, *args, **kwargs)
        return Response(semd_test_details.data)
