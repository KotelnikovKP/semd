from django.db.models import Q
from django_filters import rest_framework as filters

from backend.models.ref_inf_models import MedicalService, Diagnosis, MedicalOrganization, LaboratoryTest


def filter_medical_service_q(queryset, name, value):
    return queryset.filter(Q(name__icontains=value) | Q(ms_code__icontains=value))


def filter_medical_service_name(queryset, name, value):
    return queryset.filter(name__icontains=value)


def filter_medical_service_ms_code(queryset, name, value):
    return queryset.filter(ms_code__icontains=value)


def filter_medical_service_rel(queryset, name, value):
    return queryset.filter(rel=value)


def filter_medical_service_dateout(queryset, name, value):
    return queryset.filter(dateout=value)


class MedicalServiceFilter(filters.FilterSet):
    """
        Medical service filters
    """
    q = \
        filters.CharFilter(label='Medical service code or name for result set filtering '
                                 '(by content case insensitive).',
                           method=filter_medical_service_q)
    ms_code = \
        filters.CharFilter(label='Medical service code for result set filtering (by content case insensitive).',
                           method=filter_medical_service_ms_code)
    name = \
        filters.CharFilter(label='Medical service name for result set filtering (by content case insensitive).',
                           method=filter_medical_service_name)
    rel = \
        filters.CharFilter(label='Sign of relevance for result set filtering.',
                           method=filter_medical_service_rel)

    dateout = \
        filters.CharFilter(label='Date out for result set filtering.',
                           method=filter_medical_service_dateout)

    class Meta:
        model = MedicalService
        fields = ['ms_code', 'name', 'rel', 'dateout']


def filter_diagnosis_q(queryset, name, value):
    return queryset.filter(Q(name__icontains=value) | Q(mkb_code__icontains=value))


def filter_diagnosis_name(queryset, name, value):
    return queryset.filter(name__icontains=value)


def filter_diagnosis_mkb_code(queryset, name, value):
    return queryset.filter(mkb_code__icontains=value)


def filter_diagnosis_rel(queryset, name, value):
    return queryset.filter(rel=value)


def filter_diagnosis_dateout(queryset, name, value):
    return queryset.filter(dateout=value)


class DiagnosisFilter(filters.FilterSet):
    """
        Diagnosis filters
    """
    q = \
        filters.CharFilter(label='Diagnosis code or name for result set filtering '
                                 '(by content case insensitive).',
                           method=filter_diagnosis_q)
    mkb_code = \
        filters.CharFilter(label='Diagnosis code for result set filtering (by content case insensitive).',
                           method=filter_diagnosis_mkb_code)
    name = \
        filters.CharFilter(label='Diagnosis name for result set filtering (by content case insensitive).',
                           method=filter_diagnosis_name)
    rel = \
        filters.CharFilter(label='Sign of relevance for result set filtering.',
                           method=filter_diagnosis_rel)

    dateout = \
        filters.CharFilter(label='Date out for result set filtering.',
                           method=filter_diagnosis_dateout)

    class Meta:
        model = Diagnosis
        fields = ['mkb_code', 'name', 'rel', 'dateout']


def filter_medical_organization_q(queryset, name, value):
    return queryset.filter(Q(nameFull__icontains=value) | Q(nameShort__icontains=value) | Q(oid__icontains=value))


def filter_medical_organization_name(queryset, name, value):
    return queryset.filter(Q(nameFull__icontains=value) | Q(nameShort__icontains=value))


def filter_medical_organization_oid(queryset, name, value):
    return queryset.filter(oid__icontains=value)


def filter_medical_organization_region(queryset, name, value):
    return queryset.filter(regionId=value)


def filter_medical_organization_agency_kind(queryset, name, value):
    return queryset.filter(moAgencyKind__icontains=value)


class MedicalOrganizationFilter(filters.FilterSet):
    """
        Medical organization filters
    """
    q = \
        filters.CharFilter(label='Medical organization oid or name for result set filtering '
                                 '(by content case insensitive).',
                           method=filter_medical_organization_q)
    oid = \
        filters.CharFilter(label='Medical organization oid for result set filtering (by content case insensitive).',
                           method=filter_medical_organization_oid)
    name = \
        filters.CharFilter(label='Medical organization name for result set filtering (by content case insensitive).',
                           method=filter_medical_organization_name)
    regionId = \
        filters.CharFilter(label='Region for result set filtering.',
                           method=filter_medical_organization_region)

    moAgencyKind = \
        filters.CharFilter(label='Agency kind for result set filtering.',
                           method=filter_medical_organization_agency_kind)

    class Meta:
        model = MedicalOrganization
        fields = ['oid', 'regionId', 'moAgencyKind']


def filter_laboratory_test_q(queryset, name, value):
    return queryset.filter(Q(name__icontains=value) | Q(eng_name__icontains=value) | Q(short_name__icontains=value) |
                           Q(group_tests__icontains=value) | Q(mkb10_codes__icontains=value))


def filter_laboratory_test_id(queryset, name, value):
    return queryset.filter(id__icontains=value)


def filter_laboratory_test_group_tests(queryset, name, value):
    return queryset.filter(group_tests__icontains=value)


def filter_laboratory_test_mkb10_codes(queryset, name, value):
    return queryset.filter(mkb10_codes__icontains=value)


class LaboratoryTestFilter(filters.FilterSet):
    """
        Laboratory test filters
    """
    q = \
        filters.CharFilter(label='Laboratory test name, eng_name, short_name, group_tests or mkb10_codes '
                                 'for result set filtering (by content case insensitive).',
                           method=filter_laboratory_test_q)
    id = \
        filters.CharFilter(label='Laboratory test id for result set filtering (by content case insensitive).',
                           method=filter_laboratory_test_id)
    group_tests = \
        filters.CharFilter(label='Laboratory test group_tests for result set filtering.',
                           method=filter_laboratory_test_group_tests)

    mkb10_codes = \
        filters.CharFilter(label='Laboratory test mkb10_codes for result set filtering.',
                           method=filter_laboratory_test_mkb10_codes)

    class Meta:
        model = LaboratoryTest
        fields = ['id', 'group_tests', 'mkb10_codes']


