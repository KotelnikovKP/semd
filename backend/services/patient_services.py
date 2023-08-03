import time

from rest_framework.exceptions import ParseError, NotFound
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from backend.filters.semd_filters import SEMDFilter, SemdTestFilter
from backend.models.patient_models import PatientDiagnosis, PatientMedicalCard
from backend.models.semd_models import SEMD, SemdTest
from backend.serializers.patient_serializers import PatientListSerializer, PatientDetailsSerializer, \
    PatientSerializer, PatientDiagnosisListSerializer, PatientDiagnosisSerializer, PatientMedicalCardListSerializer, \
    PatientMedicalCardSerializer
from backend.serializers.semd_serializers import SEMDListSerializer, SemdTestListSerializer, SEMDSerializer, \
    SemdTestSerializer
from backend.serializers.serializers import PaginationListSerializer


class GetPatientListService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> PatientListSerializer:
        """
            Retrieve list of patients
        """

        # Filter queryset
        queryset = view.filter_queryset(view.get_queryset())

        # Paginate queryset
        page = view.paginate_queryset(queryset)
        if page is None:
            patient_list_serializer = view.get_serializer(queryset, many=True)
            count = view.paginator.count
            items_per_page = view.paginator.per_page
            start_item_index = 0 if count == 0 else 1
            end_item_index = count
            previous_page = None
            current_page = 1
            next_page = None
        else:
            patient_list_serializer = view.get_serializer(page, many=True)
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


class GetPatientDetailsService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> PatientDetailsSerializer:
        """
            Retrieve detail of patient
        """

        # Check input data
        snils = kwargs.get("pk", None)
        if not snils:
            raise ParseError(f"Request must have 'snils' parameter", code='snils')
        try:
            instance = view.queryset.get(snils=snils)
        except:
            raise NotFound(f"Patient with snils='{snils}' was not found", code='snils')

        # Convert data to a standard schema for a response
        patient_serializer = PatientSerializer(
            data={
                'snils': instance.snils,
                'name': instance.name,
                'gender': instance.gender,
                'birthday': instance.birthday
            },
            instance=instance
        )
        patient_serializer.is_valid()

        # Formate response schema
        return_serializer = PatientDetailsSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok',
                'result': patient_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetPatientDiagnosesService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> PatientDiagnosisListSerializer:
        """
            Retrieve diagnoses of patient
        """

        # Check input data
        snils = kwargs.get("pk", None)
        if not snils:
            raise ParseError(f"Request must have 'snils' parameter", code='snils')

        # Get queryset
        queryset = PatientDiagnosis.objects.filter(patient_id=snils).select_related('diagnosis')

        patient_diagnoses = list()
        for patient_diagnosis in queryset:
            patient_diagnosis_serializer = PatientDiagnosisSerializer(
                data={
                    "id": patient_diagnosis.id,
                },
                instance=patient_diagnosis
            )
            patient_diagnosis_serializer.is_valid()
            patient_diagnoses.append(patient_diagnosis_serializer.data)

        count = len(patient_diagnoses)
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
        return_serializer = PatientDiagnosisListSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if count > 0 else 'Result set is empty',
                'result': patient_diagnoses,
                'retExtInfo': pagination_list_serializer.data,
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetPatientMedicalCardsService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> PatientMedicalCardListSerializer:
        """
            Retrieve medical cards of patient
        """

        # Check input data
        snils = kwargs.get("pk", None)
        if not snils:
            raise ParseError(f"Request must have 'snils' parameter", code='snils')

        # Get queryset
        queryset = PatientMedicalCard.objects.filter(patient_id=snils)

        patient_medical_cards = list()
        for patient_medical_card in queryset:
            patient_medical_card_serializer = PatientMedicalCardSerializer(
                data={
                    "id": patient_medical_card.id,
                    "patient_id": patient_medical_card.patient_id,
                    "card_type": patient_medical_card.card_type,
                    "card_number": patient_medical_card.card_number
                },
                instance=patient_medical_card
            )
            patient_medical_card_serializer.is_valid()
            patient_medical_cards.append(patient_medical_card_serializer.data)

        count = len(patient_medical_cards)
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
        return_serializer = PatientMedicalCardListSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if count > 0 else 'Result set is empty',
                'result': patient_medical_cards,
                'retExtInfo': pagination_list_serializer.data,
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetPatientSemdsService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> SEMDListSerializer:
        """
            Retrieve SEMD list of patient
        """

        # Check input data
        patient_id = kwargs.get("pk", None)
        if not patient_id:
            raise ParseError(f"Request must have 'snils' parameter", code='snils')
        try:
            view.queryset.get(snils=patient_id)
        except:
            raise NotFound(f"Patient with snils='{patient_id}' was not found", code='snils')

        # Get queryset
        queryset = SEMD.objects.filter(patient_id=patient_id).order_by('patient_id', '-service_time')

        # Filter queryset
        queryset = SEMDFilter(data=request.query_params, queryset=queryset, request=request).qs

        # Paginate queryset
        page = view.paginate_queryset(queryset)
        if page is None:
            semd_list_serializer = SEMDSerializer(queryset, many=True)
            count = view.paginator.count
            items_per_page = view.paginator.per_page
            start_item_index = 0 if count == 0 else 1
            end_item_index = count
            previous_page = None
            current_page = 1
            next_page = None
        else:
            semd_list_serializer = SEMDSerializer(page, many=True)
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


class GetPatientSemdTestsService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> SemdTestListSerializer:
        """
            Retrieve laboratory test list of patient
        """

        # Check input data
        patient_id = kwargs.get("pk", None)
        if not patient_id:
            raise ParseError(f"Request must have 'snils' parameter", code='snils')
        try:
            view.queryset.get(snils=patient_id)
        except:
            raise NotFound(f"Patient with snils='{patient_id}' was not found", code='snils')

        # Get queryset
        queryset = SemdTest.objects.filter(patient_id=patient_id).order_by('patient_id', '-test_time')

        # Filter queryset
        queryset = SemdTestFilter(data=request.query_params, queryset=queryset, request=request).qs

        # Paginate queryset
        page = view.paginate_queryset(queryset)
        if page is None:
            semd_test_list_serializer = SemdTestSerializer(queryset, many=True)
            count = view.paginator.count
            items_per_page = view.paginator.per_page
            start_item_index = 0 if count == 0 else 1
            end_item_index = count
            previous_page = None
            current_page = 1
            next_page = None
        else:
            semd_test_list_serializer = SemdTestSerializer(page, many=True)
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
