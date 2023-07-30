from django.db.models import Q
from django_filters import rest_framework as filters

from backend.models.registry_models import DiagnosisRegistryItem, DiagnosisRegistry


def filter_diagnosis_registry_q(queryset, name, value):
    return queryset.filter(Q(name__icontains=value) | Q(short_name__icontains=value))


class DiagnosisRegistryFilter(filters.FilterSet):
    """
        Diagnosis registry filters
    """
    q = \
        filters.CharFilter(label='Diagnosis registry name, short name, diagnosis code and diagnosis name '
                                 'for result set filtering (by content case insensitive).',
                           method=filter_diagnosis_registry_q)

    class Meta:
        model = DiagnosisRegistry
        fields = []


def filter_diagnosis_registry_item_q(queryset, name, value):
    return queryset.filter(Q(registry__name__icontains=value) |
                           Q(registry__short_name__icontains=value) |
                           Q(diagnosis__mkb_code__icontains=value) |
                           Q(diagnosis__name__icontains=value))


class DiagnosisRegistryItemFilter(filters.FilterSet):
    """
        Diagnosis registry filters
    """
    q = \
        filters.CharFilter(label='Registry name, registry short name, diagnosis code and diagnosis name '
                                 'for result set filtering (by content case insensitive).',
                           method=filter_diagnosis_registry_item_q)

    class Meta:
        model = DiagnosisRegistryItem
        fields = []


