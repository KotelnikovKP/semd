from django.db.models import Q
from django_filters import rest_framework as filters

from backend.filters.filters import ExtraFilterSet
from backend.models.patient_models import Patient


def filter_patient_q(queryset, name, value):
    return queryset.filter(Q(name__icontains=value) | Q(snils__icontains=value))


def filter_patient_snils(queryset, name, value):
    return queryset.filter(snils=value)


def filter_patient_gender(queryset, name, value):
    return queryset.filter(gender=value)


def filter_patient_birthday(queryset, name, value):
    return queryset.filter(birthday=value)


class PatientFilter(ExtraFilterSet):
    """
        Patient filters
    """
    q = \
        filters.CharFilter(label='Patient name or snils for result set filtering '
                                 '(by content case insensitive).',
                           method=filter_patient_q)
    snils = \
        filters.CharFilter(label='Patient snils for result set filtering.',
                           method=filter_patient_snils)
    gender = \
        filters.CharFilter(label='Patient gender for result set filtering.',
                           method=filter_patient_gender)

    birthday = \
        filters.CharFilter(label='Patient mkb10_codes for result set filtering.',
                           method=filter_patient_birthday)

    class Meta:
        model = Patient
        fields = ['snils', 'gender', 'birthday']
