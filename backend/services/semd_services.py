import time

from rest_framework.exceptions import ParseError, NotFound
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from backend.models.semd_models import SemdTest
from backend.serializers.semd_serializers import SEMDListSerializer, SEMDDetailsSerializer, \
    SEMDSerializer, SemdTestListSerializer, SemdTestSerializer, SemdTestDetailsSerializer
from backend.serializers.serializers import PaginationListSerializer


class GetSemdListService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> SEMDListSerializer:
        """
            Retrieve list of SEMDs
        """

        # Filter queryset
        queryset = view.filter_queryset(view.get_queryset())

        # Paginate queryset
        page = view.paginate_queryset(queryset)
        if page is None:
            semd_list_serializer = view.get_serializer(queryset, many=True)
            count = view.paginator.count
            items_per_page = view.paginator.per_page
            start_item_index = 0 if count == 0 else 1
            end_item_index = count
            previous_page = None
            current_page = 1
            next_page = None
        else:
            semd_list_serializer = view.get_serializer(page, many=True)
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
        return_serializer = SEMDListSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if count > 0 else 'Result set is empty',
                'result': semd_list_serializer.data,
                'retExtInfo': pagination_list_serializer.data,
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetSemdDetailsService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> SEMDDetailsSerializer:
        """
            Retrieve detail of SEMD
        """

        # Check input data
        internal_message_id = kwargs.get("pk", None)
        if not internal_message_id:
            raise ParseError(f"Request must have 'internal_message_id' parameter", code='internal_message_id')
        try:
            instance = view.queryset.get(internal_message_id=internal_message_id)
        except:
            raise NotFound(f"SEMD with id='{internal_message_id}' was not found", code='internal_message_id')

        # Convert data to a standard schema for a response
        semd_serializer = SEMDSerializer(
            data={
                'internal_message_id': instance.internal_message_id,
                'document_type': instance.document_type,
                'sms_profile': instance.sms_profile,
                'date_time_create': instance.date_time_create,
                'patient_id': instance.patient_id,
                'medical_organization_id': instance.medical_organization_id,
                'doctor': instance.doctor, 
                'medical_position_id': instance.medical_position_id,
                'diagnoses': instance.diagnoses,
                'medical_service_id': instance.medical_service_id,
                'service_time': instance.service_time,
                'place_of_service': instance.place_of_service, 
                'res_protocol': instance.res_protocol, 
                'res_conclusion': instance.res_conclusion,
                'res_recommendation': instance.res_recommendation,
                'patient_condition': instance.patient_condition, 
                'patient_diagnosis_id': instance.patient_diagnosis_id,
                'patient_in_condition': instance.patient_in_condition,
                'patient_out_condition': instance.patient_out_condition,
                'start_date': instance.start_date, 
                'end_date': instance.end_date,
                'hospitalization_results': instance.hospitalization_results, 
                'hospitalization_urgency': instance.hospitalization_urgency
            },
            instance=instance
        )
        semd_serializer.is_valid()

        # Formate response schema
        return_serializer = SEMDDetailsSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok',
                'result': semd_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetSemdTestsService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> SemdTestListSerializer:
        """
            Retrieve tests of SEMD
        """

        # Check input data
        internal_message_id = kwargs.get("pk", None)
        if not internal_message_id:
            raise ParseError(f"Request must have 'internal_message_id' parameter", code='internal_message_id')

        # Get queryset
        queryset = SemdTest.objects.filter(semd_id=internal_message_id)

        semd_tests = list()
        for semd_test in queryset:
            semd_test_serializer = SemdTestSerializer(
                data={
                    "id": semd_test.id,
                },
                instance=semd_test
            )
            semd_test_serializer.is_valid()
            semd_tests.append(semd_test_serializer.data)

        count = len(semd_tests)
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
        return_serializer = SemdTestListSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if count > 0 else 'Result set is empty',
                'result': semd_tests,
                'retExtInfo': pagination_list_serializer.data,
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetSemdTestListService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> SemdTestListSerializer:
        """
            Retrieve list of SEMD tests
        """

        # Filter queryset
        queryset = view.filter_queryset(view.get_queryset())

        # Paginate queryset
        page = view.paginate_queryset(queryset)
        if page is None:
            semd_test_list_serializer = view.get_serializer(queryset, many=True)
            count = view.paginator.count
            items_per_page = view.paginator.per_page
            start_item_index = 0 if count == 0 else 1
            end_item_index = count
            previous_page = None
            current_page = 1
            next_page = None
        else:
            semd_test_list_serializer = view.get_serializer(page, many=True)
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
        return_serializer = SemdTestListSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if count > 0 else 'Result set is empty',
                'result': semd_test_list_serializer.data,
                'retExtInfo': pagination_list_serializer.data,
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetSemdTestDetailsService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> SemdTestDetailsSerializer:
        """
            Retrieve detail of SEMD test
        """

        # Check input data
        id = kwargs.get("pk", None)
        if not id:
            raise ParseError(f"Request must have 'id' parameter", code='id')
        try:
            instance = view.queryset.get(id=id)
        except:
            raise NotFound(f"SemdTest with id='{id}' was not found", code='id')

        # Convert data to a standard schema for a response
        semd_test_serializer = SemdTestSerializer(
            data={
                'id': instance.id,
                'semd_id': instance.semd_id,
                'test_time': instance.test_time,
                'patient_id': instance.patient_id,
                'laboratory_test_id': instance.laboratory_test_id,
                'value': instance.value
            },
            instance=instance
        )
        semd_test_serializer.is_valid()

        # Formate response schema
        return_serializer = SemdTestDetailsSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok',
                'result': semd_test_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer
