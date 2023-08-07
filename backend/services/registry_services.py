import time

from django.db.models import Exists, OuterRef
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from backend.filters.patient_filters import PatientFilter
from backend.models.patient_models import PatientDiagnosis, Patient
from backend.models.registry_models import DiagnosisRegistryItem
from backend.serializers.patient_serializers import PatientListSerializer, PatientSerializer
from backend.serializers.registry_serializers import DiagnosisRegistryListSerializer, DiagnosisRegistrySerializer, \
    DiagnosisRegistrySingleEntrySerializer, DiagnosisRegistryItemListSerializer, \
    DiagnosisRegistryItemSingleEntrySerializer, DiagnosisRegistryItemSerializer
from backend.serializers.serializers import PaginationListSerializer


class GetDiagnosisRegistryListService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> DiagnosisRegistryListSerializer:
        """
            Retrieve list of diagnosis registry
        """

        # Filter queryset
        queryset = view.filter_queryset(view.get_queryset())

        # Paginate queryset
        page = view.paginate_queryset(queryset)
        if page is None:
            diagnosis_registry_list_serializer = view.get_serializer(queryset, many=True)
            count = view.paginator.count
            items_per_page = view.paginator.per_page
            start_item_index = 0 if count == 0 else 1
            end_item_index = count
            previous_page = None
            current_page = 1
            next_page = None
        else:
            diagnosis_registry_list_serializer = view.get_serializer(page, many=True)
            count = view.paginator.page.paginator.count
            items_per_page = view.paginator.page.paginator.per_page
            start_item_index = view.paginator.page.start_index()
            end_item_index = view.paginator.page.end_index()
            previous_page = view.paginator.page.previous_page_number() if view.paginator.page.has_previous() else None
            current_page = view.paginator.page.number
            next_page = view.paginator.page.next_page_number() if view.paginator.page.has_next() else None

        # Formate pagination list's extra information schema
        pagination_list_serializer = PaginationListSerializer(
            data={
                'count_items': count,
                'items_per_page': items_per_page,
                'start_item_index': start_item_index,
                'end_item_index': end_item_index,
                'previous_page': previous_page,
                'current_page': current_page,
                'next_page': next_page,
            }
        )
        pagination_list_serializer.is_valid()

        # Formate response schema
        return_serializer = DiagnosisRegistryListSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if count > 0 else 'Result set is empty',
                'result': diagnosis_registry_list_serializer.data,
                'retExtInfo': pagination_list_serializer.data,
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class CreateDiagnosisRegistryService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> DiagnosisRegistrySingleEntrySerializer:
        """
            Create diagnosis registry
        """

        # Check and save input data
        diagnosis_registry_serializer = DiagnosisRegistrySerializer(data=request.data)
        diagnosis_registry_serializer.is_valid(raise_exception=True)
        diagnosis_registry_serializer.save()

        # Formate response schema
        return_serializer = DiagnosisRegistrySingleEntrySerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok',
                'result': diagnosis_registry_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetDiagnosisRegistryDetailsService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> DiagnosisRegistrySingleEntrySerializer:
        """
            Retrieve detail of diagnosis registry
        """

        # Check input data
        pk = kwargs.get("pk", None)
        if not pk:
            raise ParseError(f"Request must have 'id' parameter", code='id')
        try:
            instance = view.queryset.get(pk=pk)
        except:
            raise NotFound(f"Diagnosis registry with id='{pk}' was not found", code='id')

        # Convert data to a standard schema for a response
        diagnosis_registry_serializer = DiagnosisRegistrySerializer(
            data={
                'id': instance.id,
                'name': instance.name,
                'short_name': instance.short_name,
                'medical_record_transcript_settings': instance.medical_record_transcript_settings,
            },
            instance=instance
        )
        diagnosis_registry_serializer.is_valid()

        # Formate response schema
        return_serializer = DiagnosisRegistrySingleEntrySerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok',
                'result': diagnosis_registry_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetDiagnosisRegistryDiagnosesService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> DiagnosisRegistryItemListSerializer:
        """
            Retrieve diagnoses list of diagnosis registry
        """

        # Check input data
        pk = kwargs.get("pk", None)
        if not pk:
            raise ParseError(f"Request must have 'id' parameter", code='id')
        try:
            view.queryset.get(pk=pk)
        except:
            raise NotFound(f"Diagnosis registry with id='{pk}' was not found", code='id')

        # Get queryset
        queryset = DiagnosisRegistryItem.objects.filter(registry_id=pk)

        diagnosis_registry_items = list()
        for diagnosis_registry_item in queryset:
            diagnosis_registry_item_serializer = DiagnosisRegistryItemSerializer(
                data={
                    'id': diagnosis_registry_item.id,
                    'registry': diagnosis_registry_item.registry_id,
                    'diagnosis': diagnosis_registry_item.diagnosis_id
                },
                instance=diagnosis_registry_item
            )
            diagnosis_registry_item_serializer.is_valid()
            diagnosis_registry_items.append(diagnosis_registry_item_serializer.data)

        count = len(diagnosis_registry_items)
        items_per_page = count
        start_item_index = 0 if count == 0 else 1
        end_item_index = count
        previous_page = None
        current_page = 1
        next_page = None

        # Formate pagination list's extra information schema
        pagination_list_serializer = PaginationListSerializer(
            data={
                'count_items': count,
                'items_per_page': items_per_page,
                'start_item_index': start_item_index,
                'end_item_index': end_item_index,
                'previous_page': previous_page,
                'current_page': current_page,
                'next_page': next_page,
            }
        )
        pagination_list_serializer.is_valid()

        # Formate response schema
        return_serializer = DiagnosisRegistryItemListSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if count > 0 else 'Result set is empty',
                'result': diagnosis_registry_items,
                'retExtInfo': pagination_list_serializer.data,
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetDiagnosisRegistryPatientsService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> PatientListSerializer:
        """
            Retrieve patient list of diagnosis registry
        """

        # Check input data
        pk = kwargs.get("pk", None)
        if not pk:
            raise ParseError(f"Request must have 'id' parameter", code='id')
        try:
            view.queryset.get(pk=pk)
        except:
            raise NotFound(f"Diagnosis registry with id='{pk}' was not found", code='id')

        # Get queryset
        queryset = Patient.objects.filter(
            Exists(
                PatientDiagnosis.objects.filter(
                    patient=OuterRef('pk'),
                    diagnosis_id__in=[
                        diagnosis_registry_item.diagnosis_id
                        for diagnosis_registry_item in DiagnosisRegistryItem.objects.filter(registry_id=pk)
                    ]
                )
            )
        )

        # Filter queryset
        queryset = PatientFilter(data=request.query_params, queryset=queryset, request=request).qs

        # Paginate queryset
        page = view.paginate_queryset(queryset)
        if page is None:
            patient_list_serializer = PatientSerializer(queryset, many=True)
            count = view.paginator.count
            items_per_page = view.paginator.per_page
            start_item_index = 0 if count == 0 else 1
            end_item_index = count
            previous_page = None
            current_page = 1
            next_page = None
        else:
            patient_list_serializer = PatientSerializer(page, many=True)
            count = view.paginator.page.paginator.count
            items_per_page = view.paginator.page.paginator.per_page
            start_item_index = view.paginator.page.start_index()
            end_item_index = view.paginator.page.end_index()
            previous_page = view.paginator.page.previous_page_number() if view.paginator.page.has_previous() else None
            current_page = view.paginator.page.number
            next_page = view.paginator.page.next_page_number() if view.paginator.page.has_next() else None

        # Formate pagination list's extra information schema
        pagination_list_serializer = PaginationListSerializer(
            data={
                'count_items': count,
                'items_per_page': items_per_page,
                'start_item_index': start_item_index,
                'end_item_index': end_item_index,
                'previous_page': previous_page,
                'current_page': current_page,
                'next_page': next_page,
            }
        )
        pagination_list_serializer.is_valid()

        # Formate response schema
        return_serializer = PatientListSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if count > 0 else 'Result set is empty',
                'result': patient_list_serializer.data,
                'retExtInfo': pagination_list_serializer.data,
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class UpdateDiagnosisRegistryService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> DiagnosisRegistrySingleEntrySerializer:
        """
            Update diagnosis registry
        """

        # Check and save input data
        pk = kwargs.get("pk", None)
        if not pk:
            raise ParseError(f"Request must have 'id' parameter", code='id')
        try:
            instance = view.queryset.get(pk=pk)
        except:
            raise NotFound(f"Diagnosis registry with id='{pk}' was not found", code='id')

        diagnosis_registry_serializer = DiagnosisRegistrySerializer(data=request.data, instance=instance)
        diagnosis_registry_serializer.is_valid(raise_exception=True)
        diagnosis_registry_serializer.save()

        # Formate response schema
        is_data = request.data.get('name', None) is not None or \
            request.data.get('short_name', None) is not None
        return_serializer = DiagnosisRegistrySingleEntrySerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if is_data else 'You changed nothing',
                'result': diagnosis_registry_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class DeleteDiagnosisRegistryService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> DiagnosisRegistrySingleEntrySerializer:
        """
            Delete diagnosis registry
        """

        # Check input data
        pk = kwargs.get("pk", None)
        if not pk:
            raise ParseError(f"Request must have 'id' parameter", code='id')
        try:
            instance = view.queryset.get(pk=pk)
        except:
            raise NotFound(f"Diagnosis registry with id='{pk}' was not found", code='id')

        # Delete diagnosis registry
        instance.delete()

        # Formate response schema
        return_serializer = DiagnosisRegistrySingleEntrySerializer(
            data={
                'retCode': 0,
                'retMsg': f'Ok. Diagnosis registry with id={pk} was deleted',
                'result': {},
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetDiagnosisRegistryItemListService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> DiagnosisRegistryItemListSerializer:
        """
            Retrieve list of diagnosis registry item
        """

        # Filter queryset
        queryset = view.filter_queryset(view.get_queryset())

        # Paginate queryset
        page = view.paginate_queryset(queryset)
        if page is None:
            diagnosis_registry_item_list_serializer = view.get_serializer(queryset, many=True)
            count = view.paginator.count
            items_per_page = view.paginator.per_page
            start_item_index = 0 if count == 0 else 1
            end_item_index = count
            previous_page = None
            current_page = 1
            next_page = None
        else:
            diagnosis_registry_item_list_serializer = view.get_serializer(page, many=True)
            count = view.paginator.page.paginator.count
            items_per_page = view.paginator.page.paginator.per_page
            start_item_index = view.paginator.page.start_index()
            end_item_index = view.paginator.page.end_index()
            previous_page = view.paginator.page.previous_page_number() if view.paginator.page.has_previous() else None
            current_page = view.paginator.page.number
            next_page = view.paginator.page.next_page_number() if view.paginator.page.has_next() else None

        # Formate pagination list's extra information schema
        pagination_list_serializer = PaginationListSerializer(
            data={
                'count_items': count,
                'items_per_page': items_per_page,
                'start_item_index': start_item_index,
                'end_item_index': end_item_index,
                'previous_page': previous_page,
                'current_page': current_page,
                'next_page': next_page,
            }
        )
        pagination_list_serializer.is_valid()

        # Formate response schema
        return_serializer = DiagnosisRegistryItemListSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if count > 0 else 'Result set is empty',
                'result': diagnosis_registry_item_list_serializer.data,
                'retExtInfo': pagination_list_serializer.data,
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class CreateDiagnosisRegistryItemService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> DiagnosisRegistryItemSingleEntrySerializer:
        """
            Create diagnosis registry item
        """

        # Check and save input data
        diagnosis_registry_item_serializer = DiagnosisRegistryItemSerializer(data=request.data)
        diagnosis_registry_item_serializer.is_valid(raise_exception=True)
        diagnosis_registry_item_serializer.save()

        # Formate response schema
        return_serializer = DiagnosisRegistryItemSingleEntrySerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok',
                'result': diagnosis_registry_item_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetDiagnosisRegistryItemDetailsService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> DiagnosisRegistryItemSingleEntrySerializer:
        """
            Retrieve detail of diagnosis registry item
        """

        # Check input data
        pk = kwargs.get("pk", None)
        if not pk:
            raise ParseError(f"Request must have 'id' parameter", code='id')
        try:
            instance = view.queryset.get(pk=pk)
        except:
            raise NotFound(f"Diagnosis registry item with id='{pk}' was not found", code='id')

        # Convert data to a standard schema for a response
        diagnosis_registry_item_serializer = DiagnosisRegistryItemSerializer(
            data={
                'id': instance.id,
                'registry': instance.registry_id,
                'diagnosis': instance.diagnosis_id
            },
            instance=instance
        )
        diagnosis_registry_item_serializer.is_valid()

        # Formate response schema
        return_serializer = DiagnosisRegistryItemSingleEntrySerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok',
                'result': diagnosis_registry_item_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class UpdateDiagnosisRegistryItemService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> DiagnosisRegistryItemSingleEntrySerializer:
        """
            Update diagnosis registry item
        """

        # Check and save input data
        pk = kwargs.get("pk", None)
        if not pk:
            raise ParseError(f"Request must have 'id' parameter", code='id')
        try:
            instance = view.queryset.get(pk=pk)
        except:
            raise NotFound(f"Diagnosis registry item with id='{pk}' was not found", code='id')

        diagnosis_registry_item_serializer = DiagnosisRegistryItemSerializer(data=request.data, instance=instance)
        diagnosis_registry_item_serializer.is_valid(raise_exception=True)
        diagnosis_registry_item_serializer.save()

        # Formate response schema
        is_data = request.data.get('registry_id', None) is not None or \
            request.data.get('diagnosis_id', None) is not None
        return_serializer = DiagnosisRegistryItemSingleEntrySerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if is_data else 'You changed nothing',
                'result': diagnosis_registry_item_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class DeleteDiagnosisRegistryItemService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> DiagnosisRegistryItemSingleEntrySerializer:
        """
            Delete diagnosis registry item
        """

        # Check input data
        pk = kwargs.get("pk", None)
        if not pk:
            raise ParseError(f"Request must have 'id' parameter", code='id')
        try:
            instance = view.queryset.get(pk=pk)
        except:
            raise NotFound(f"Diagnosis registry item with id='{pk}' was not found", code='id')

        # Delete diagnosis registry
        instance.delete()

        # Formate response schema
        return_serializer = DiagnosisRegistryItemSingleEntrySerializer(
            data={
                'retCode': 0,
                'retMsg': f'Ok. Diagnosis registry item with id={pk} was deleted',
                'result': {},
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer

