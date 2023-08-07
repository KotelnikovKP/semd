from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from backend.filters.patient_filters import PatientFilter
from backend.filters.registry_filters import DiagnosisRegistryFilter, DiagnosisRegistryItemFilter
from backend.helpers import expand_dict
from backend.models.registry_models import DiagnosisRegistry, DiagnosisRegistryItem
from backend.permissions.registry_permission import DiagnosisRegistryPermission, DiagnosisRegistryItemPermission
from backend.serializers.patient_serializers import PatientListSerializer
from backend.serializers.registry_serializers import DiagnosisRegistrySerializer, DiagnosisRegistryListSerializer, \
    DiagnosisRegistrySingleEntrySerializer, DiagnosisRegistryItemSerializer, DiagnosisRegistryItemListSerializer, \
    DiagnosisRegistryItemSingleEntrySerializer
from backend.serializers.serializers import simple_responses
from backend.services.registry_services import GetDiagnosisRegistryListService, CreateDiagnosisRegistryService, \
    GetDiagnosisRegistryDetailsService, UpdateDiagnosisRegistryService, DeleteDiagnosisRegistryService, \
    GetDiagnosisRegistryItemListService, CreateDiagnosisRegistryItemService, GetDiagnosisRegistryItemDetailsService, \
    UpdateDiagnosisRegistryItemService, DeleteDiagnosisRegistryItemService, GetDiagnosisRegistryDiagnosesService, \
    GetDiagnosisRegistryPatientsService


@extend_schema(tags=['Diagnosis registry'])
class DiagnosisRegistryViewSet(ModelViewSet):

    permission_classes = (DiagnosisRegistryPermission, )
    queryset = DiagnosisRegistry.objects.all()
    serializer_class = DiagnosisRegistrySerializer
    filterset_class = DiagnosisRegistryFilter

    @extend_schema(
        summary='Retrieve paginated and filtered list of diagnosis registers',
        description='Retrieve paginated and filtered list of diagnosis registers, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: DiagnosisRegistryListSerializer, }, simple_responses),
    )
    def list(self, request, *args, **kwargs):
        """
            Retrieve list of diagnosis registers
        """
        diagnosis_registry_list = GetDiagnosisRegistryListService.execute(request, self, *args, **kwargs)
        return Response(diagnosis_registry_list.data)

    @extend_schema(
        summary='Create diagnosis registry',
        description='Create diagnosis registry, bla-bla-bla...',
        request=DiagnosisRegistrySerializer,
        responses=expand_dict({status.HTTP_200_OK: DiagnosisRegistrySingleEntrySerializer, }, simple_responses),
    )
    def create(self, request, *args, **kwargs):
        """
            Create diagnosis registry
        """
        diagnosis_registry_create = CreateDiagnosisRegistryService.execute(request, self, *args, **kwargs)
        return Response(diagnosis_registry_create.data)

    @extend_schema(
        summary='Retrieve diagnosis registry details',
        description='Retrieve diagnosis registry details, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: DiagnosisRegistrySingleEntrySerializer, }, simple_responses),
    )
    def retrieve(self, request, *args, **kwargs):
        """
            Retrieve detail of diagnosis registry
        """
        diagnosis_registry_details = GetDiagnosisRegistryDetailsService.execute(request, self, *args, **kwargs)
        return Response(diagnosis_registry_details.data)

    @extend_schema(
        summary='Retrieve diagnoses list of diagnosis registry',
        description='Retrieve diagnoses list of diagnosis registry, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: DiagnosisRegistryItemListSerializer, }, simple_responses),
    )
    @action(detail=True)
    def diagnoses(self, request, *args, **kwargs):
        """
            Retrieve diagnoses list of diagnosis registry
        """
        diagnosis_registry_items = GetDiagnosisRegistryDiagnosesService.execute(request, self, *args, **kwargs)
        return Response(diagnosis_registry_items.data)

    @extend_schema(
        summary='Retrieve paginated and filtered patients list of diagnosis registry',
        description='Retrieve paginated and filtered patients list of diagnosis registry, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: PatientListSerializer, }, simple_responses),
        parameters=[OpenApiParameter('page', OpenApiTypes.INT, OpenApiParameter.QUERY,
                                     description='A page number within the paginated result set.')] +
        PatientFilter.get_api_filters(),
    )
    @action(detail=True)
    def patients(self, request, *args, **kwargs):
        """
            Retrieve paginated and filtered patients list of diagnosis registry
        """
        diagnosis_registry_patients = GetDiagnosisRegistryPatientsService.execute(request, self, *args, **kwargs)
        return Response(diagnosis_registry_patients.data)

    @extend_schema(
        summary='Update diagnosis registry',
        description='Update diagnosis registry, bla-bla-bla...',
        request=DiagnosisRegistrySerializer,
        responses=expand_dict({status.HTTP_200_OK: DiagnosisRegistrySingleEntrySerializer, }, simple_responses),
    )
    def update(self, request, *args, **kwargs):
        """
            Update diagnosis registry
        """
        diagnosis_registry_update = UpdateDiagnosisRegistryService.execute(request, self, *args, **kwargs)
        return Response(diagnosis_registry_update.data)

    @extend_schema(
        summary='Delete diagnosis registry',
        description='Delete diagnosis registry, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: DiagnosisRegistrySingleEntrySerializer, }, simple_responses),
    )
    def destroy(self, request,  *args, **kwargs):
        """
            Delete diagnosis registry
        """
        diagnosis_registry_delete = DeleteDiagnosisRegistryService.execute(request, self, *args, **kwargs)
        return Response(diagnosis_registry_delete.data)


@extend_schema(tags=['Diagnosis registry'])
class DiagnosisRegistryItemViewSet(ModelViewSet):

    permission_classes = (DiagnosisRegistryItemPermission, )
    queryset = DiagnosisRegistryItem.objects.all()
    serializer_class = DiagnosisRegistryItemSerializer
    filterset_class = DiagnosisRegistryItemFilter

    @extend_schema(
        summary='Retrieve paginated and filtered list of diagnosis registry items',
        description='Retrieve paginated and filtered list of diagnosis registry items, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: DiagnosisRegistryItemListSerializer, }, simple_responses),
    )
    def list(self, request, *args, **kwargs):
        """
            Retrieve list of diagnosis registry items
        """
        diagnosis_registry_item_list = GetDiagnosisRegistryItemListService.execute(request, self, *args, **kwargs)
        return Response(diagnosis_registry_item_list.data)

    @extend_schema(
        summary='Create diagnosis registry item',
        description='Create diagnosis registry item, bla-bla-bla...',
        request=DiagnosisRegistryItemSerializer,
        responses=expand_dict({status.HTTP_200_OK: DiagnosisRegistryItemSingleEntrySerializer, }, simple_responses),
    )
    def create(self, request, *args, **kwargs):
        """
            Create diagnosis registry item
        """
        diagnosis_registry_item_create = CreateDiagnosisRegistryItemService.execute(request, self, *args, **kwargs)
        return Response(diagnosis_registry_item_create.data)

    @extend_schema(
        summary='Retrieve diagnosis registry item details',
        description='Retrieve diagnosis registry item details, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: DiagnosisRegistryItemSingleEntrySerializer, }, simple_responses),
    )
    def retrieve(self, request, *args, **kwargs):
        """
            Retrieve detail of diagnosis registry item
        """
        diagnosis_registry_item_details = GetDiagnosisRegistryItemDetailsService.execute(request, self, *args, **kwargs)
        return Response(diagnosis_registry_item_details.data)

    @extend_schema(
        summary='Update diagnosis registry item',
        description='Update diagnosis registry item, bla-bla-bla...',
        request=DiagnosisRegistryItemSerializer,
        responses=expand_dict({status.HTTP_200_OK: DiagnosisRegistryItemSingleEntrySerializer, }, simple_responses),
    )
    def update(self, request, *args, **kwargs):
        """
            Update diagnosis registry item
        """
        diagnosis_registry_item_update = UpdateDiagnosisRegistryItemService.execute(request, self, *args, **kwargs)
        return Response(diagnosis_registry_item_update.data)

    @extend_schema(
        summary='Delete diagnosis registry item',
        description='Delete diagnosis registry item, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: DiagnosisRegistryItemSingleEntrySerializer, }, simple_responses),
    )
    def destroy(self, request,  *args, **kwargs):
        """
            Delete diagnosis registry item
        """
        diagnosis_registry_item_delete = DeleteDiagnosisRegistryItemService.execute(request, self, *args, **kwargs)
        return Response(diagnosis_registry_item_delete.data)


