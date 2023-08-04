from django.db.models import Q
from django_filters import rest_framework as filters, DateTimeFromToRangeFilter

from backend.models.semd_models import SEMD, SemdTest


def filter_semd_q(queryset, name, value):
    return queryset.filter(Q(patient__name__icontains=value)
                           | Q(patient__snils__icontains=value)
                           | Q(diagnoses__icontains=value)
                           | Q(patient_diagnosis__name__icontains=value)
                           | Q(doctor__icontains=value)
                           | Q(medical_service__ms_code__icontains=value)
                           | Q(medical_position__name__icontains=value)
                           | Q(medical_service__name__icontains=value)
                           | Q(medical_organization__nameShort__icontains=value)
                           )


def filter_semd_internal_message_id(queryset, name, value):
    return queryset.filter(internal_message_id=value)


def filter_semd_document_type(queryset, name, value):
    return queryset.filter(document_type=value)


def filter_semd_sms_profile(queryset, name, value):
    return queryset.filter(sms_profile=value)


def filter_semd_patient_id(queryset, name, value):
    return queryset.filter(patient_id=value)


def filter_semd_medical_organization_id(queryset, name, value):
    return queryset.filter(medical_organization_id=value)


def filter_semd_medical_service_id(queryset, name, value):
    return queryset.filter(medical_service_id=value)


class SEMDFilter(filters.FilterSet):
    """
        SEMD filters
    """
    q = \
        filters.CharFilter(label='SEMD name or snils patient or diagnosis or name or job doctor or '
                                 'medical organization or medical service for result set filtering '
                                 '(by content case insensitive).',
                           method=filter_semd_q)
    internal_message_id = \
        filters.CharFilter(label='SEMD id for result set filtering.',
                           method=filter_semd_internal_message_id)

    document_type = \
        filters.CharFilter(label='SEMD document type for result set filtering.',
                           method=filter_semd_document_type)
    sms_profile = \
        filters.CharFilter(label='SEMD profile for result set filtering.',
                           method=filter_semd_sms_profile)

    patient_id = \
        filters.CharFilter(label='SEMD patient SNILS for result set filtering.',
                           method=filter_semd_patient_id)

    medical_organization_id = \
        filters.CharFilter(label='SEMD medical organization id for result set filtering.',
                           method=filter_semd_medical_organization_id)

    medical_service_id = \
        filters.CharFilter(label='SEMD medical service id for result set filtering.',
                           method=filter_semd_medical_service_id)

    service_time = DateTimeFromToRangeFilter(label='SEMD service time range for result set filtering.')

    date_time_create = DateTimeFromToRangeFilter(label='SEMD create time range for result set filtering.')

    class Meta:
        model = SEMD
        fields = ['internal_message_id', 'document_type', 'sms_profile', 'patient_id', 'medical_organization_id',
                  'medical_service_id', 'service_time', 'date_time_create']


def filter_semd_test_q(queryset, name, value):
    # name or snils patient or SEMD id or laboratory test
    return queryset.filter(
        Q(patient__name__icontains=value)
        | Q(patient__snils__icontains=value)
        | Q(semd__internal_message_id__icontains=value)
        | Q(laboratory_test__name__icontains=value)
    )


def filter_semd_test_id(queryset, name, value):
    return queryset.filter(id=value)


def filter_semd_test_semd_id(queryset, name, value):
    return queryset.filter(semd_id=value)


def filter_semd_test_laboratory_test_id(queryset, name, value):
    return queryset.filter(laboratory_test_id=value)


def filter_semd_test_patient_id(queryset, name, value):
    return queryset.filter(patient_id=value)


class SemdTestFilter(filters.FilterSet):
    """
        SEMD test filters
    """
    q = \
        filters.CharFilter(label='SEMD test name or snils patient or SEMD id or laboratory test '
                                 'for result set filtering (by content case insensitive).',
                           method=filter_semd_test_q)
    id = \
        filters.CharFilter(label='SEMD test id for result set filtering.',
                           method=filter_semd_test_id)

    semd_id = \
        filters.CharFilter(label='SEMD test SEMD id for result set filtering.',
                           method=filter_semd_test_semd_id)

    patient_id = \
        filters.CharFilter(label='SEMD test patient SNILS for result set filtering.',
                           method=filter_semd_test_patient_id)

    laboratory_test_id = \
        filters.CharFilter(label='SEMD test laboratory test id for result set filtering.',
                           method=filter_semd_test_laboratory_test_id)

    test_time = DateTimeFromToRangeFilter(label='SEMD test time range for result set filtering.')

    class Meta:
        model = SemdTest
        fields = ['id', 'semd_id', 'patient_id', 'laboratory_test_id', 'test_time']
