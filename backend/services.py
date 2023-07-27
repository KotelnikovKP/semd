import time

from rest_framework.exceptions import ParseError, NotFound
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from backend.serializers import UserRegisterSerializer, UserSerializer, UserCreateSerializer, \
    MedicalServiceListSerializer, PaginationListSerializer, DiagnosisListSerializer, MedicalOrganizationListSerializer


class CreateUserService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> UserCreateSerializer:
        """
            User registration
        """

        # Check and save input data
        user_serializer = UserRegisterSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        instance = user_serializer.save()

        # Convert data to a standard schema for a response
        user_serializer = UserSerializer(data=user_serializer.data, instance=instance)
        user_serializer.is_valid()

        # Formate response schema
        return_serializer = UserCreateSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok',
                'result': user_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetUserDetailsService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> UserSerializer:
        """
            Retrieve user profile
        """

        # Check input data
        try:
            pk = request.user.pk
        except:
            raise ParseError(f"Request must have 'user' parameter", code='id')
        try:
            instance = view.queryset.get(pk=pk)
        except:
            raise NotFound(f"User with id='{pk}' was not found", code='id')

        # Formate response schema
        user_serializer = UserSerializer(
            data={
                'id': instance.id,
                'username': instance.username,
                'first_name': instance.first_name,
                'last_name': instance.last_name,
                'email': instance.email,
            },
            instance=instance
        )
        user_serializer.is_valid()

        return user_serializer


class GetMedicalServiceListService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> MedicalServiceListSerializer:
        """
            Retrieve list of medical services
        """

        # Filter queryset
        queryset = view.filter_queryset(view.get_queryset())

        # Paginate queryset
        page = view.paginate_queryset(queryset)
        if page is None:
            medical_service_list_serializer = view.get_serializer(queryset, many=True)
            count = view.paginator.count
            items_per_page = view.paginator.per_page
            start_item_index = 0 if count == 0 else 1
            end_item_index = count
            previous_page = None
            current_page = 1
            next_page = None
        else:
            medical_service_list_serializer = view.get_serializer(page, many=True)
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
        return_serializer = MedicalServiceListSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if count > 0 else 'Result set is empty',
                'result': medical_service_list_serializer.data,
                'retExtInfo': pagination_list_serializer.data,
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetDiagnosisListService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> DiagnosisListSerializer:
        """
            Retrieve list of diagnoses
        """

        # Filter queryset
        queryset = view.filter_queryset(view.get_queryset())

        # Paginate queryset
        page = view.paginate_queryset(queryset)
        if page is None:
            diagnosis_list_serializer = view.get_serializer(queryset, many=True)
            count = view.paginator.count
            items_per_page = view.paginator.per_page
            start_item_index = 0 if count == 0 else 1
            end_item_index = count
            previous_page = None
            current_page = 1
            next_page = None
        else:
            diagnosis_list_serializer = view.get_serializer(page, many=True)
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
        return_serializer = DiagnosisListSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if count > 0 else 'Result set is empty',
                'result': diagnosis_list_serializer.data,
                'retExtInfo': pagination_list_serializer.data,
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetMedicalOrganizationListService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> MedicalOrganizationListSerializer:
        """
            Retrieve list of diagnoses
        """

        # Filter queryset
        queryset = view.filter_queryset(view.get_queryset())

        # Paginate queryset
        page = view.paginate_queryset(queryset)
        if page is None:
            medical_organization_list_serializer = view.get_serializer(queryset, many=True)
            count = view.paginator.count
            items_per_page = view.paginator.per_page
            start_item_index = 0 if count == 0 else 1
            end_item_index = count
            previous_page = None
            current_page = 1
            next_page = None
        else:
            medical_organization_list_serializer = view.get_serializer(page, many=True)
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
        return_serializer = MedicalOrganizationListSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if count > 0 else 'Result set is empty',
                'result': medical_organization_list_serializer.data,
                'retExtInfo': pagination_list_serializer.data,
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer