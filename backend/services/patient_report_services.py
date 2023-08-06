import time
from datetime import datetime

from rest_framework.exceptions import ParseError, NotFound
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from backend.models.registry_models import DiagnosisRegistry
from backend.models.semd_models import SEMD, SemdTest
from backend.serializers.patient_serializers import PatientRegistryReportDetailSerializer, \
    PatientRegistryReportSerializer
from backend.serializers.semd_serializers import SEMDSerializer, SemdTestSerializer


class GetPatientRegistryReportService:
    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> PatientRegistryReportDetailSerializer:
        """
            Retrieve registry report of patient
        """

        # Check input data
        patient_id = kwargs.get("pk", None)
        if not patient_id:
            raise ParseError(f"Request must have 'snils' parameter", code='snils')
        diagnosis_registry_id = request.query_params.get("diagnosis_registry_id", None)
        if not diagnosis_registry_id:
            raise ParseError(f"Request must have 'diagnosis_registry_id' query parameter", code='diagnosis_registry_id')
        try:
            view.queryset.get(snils=patient_id)
        except:
            raise NotFound(f"Patient with snils='{patient_id}' was not found", code='snils')
        try:
            diagnosis_registry = DiagnosisRegistry.objects.get(id=diagnosis_registry_id)
            registry_report_settings = diagnosis_registry.medical_record_transcript_settings
        except:
            raise NotFound(f"Diagnosis registry with id='{diagnosis_registry_id}' was not found",
                           code='diagnosis_registry_id')

        # Get querysets
        events_queryset = GetPatientRegistryReportService._get_semds(
            patient_id, registry_report_settings, 'Events', grouped=False
        )
        medical_tests_queryset = GetPatientRegistryReportService._get_semd_tests(
            patient_id, registry_report_settings, 'MedicalTests', grouped=True
        )
        medical_examinations_queryset = GetPatientRegistryReportService._get_semds(
            patient_id, registry_report_settings, 'MedicalExaminations', grouped=True
        )
        treatment_queryset = GetPatientRegistryReportService._get_semds(
            patient_id, registry_report_settings, 'Treatment', grouped=True
        )
        recommended_therapy_queryset = GetPatientRegistryReportService._get_semds(
            patient_id, registry_report_settings, 'RecommendedTherapy', grouped=True
        )

        # Serialize querysets
        events_serializer = SEMDSerializer(events_queryset, many=True)
        medical_tests_serializer = SemdTestSerializer(medical_tests_queryset, many=True)
        medical_examinations_serializer = SEMDSerializer(medical_examinations_queryset, many=True)
        treatment_serializer = SEMDSerializer(treatment_queryset, many=True)
        recommended_therapy_serializer = SEMDSerializer(recommended_therapy_queryset, many=True)

        # Convert data to a standard schema for a response
        patient_registry_report_serializer = PatientRegistryReportSerializer(
            data={
                'events': events_serializer.data,
                'medical_tests': medical_tests_serializer.data,
                'medical_examinations': medical_examinations_serializer.data,
                'treatment': treatment_serializer.data,
                'recommended_therapy': recommended_therapy_serializer.data,
            },
        )
        # patient_registry_report_serializer.is_valid()

        # Formate response schema
        return_serializer = PatientRegistryReportDetailSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok',
                'result': patient_registry_report_serializer.initial_data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer

    @staticmethod
    def _get_semds(patient_id, registry_report_settings, section, grouped=False):
        print(f'GET SEMDs, section={section}')
        settings = registry_report_settings.get(section, None)
        if settings:
            records = settings.get('records', None)
            if records:
                ids = set()
                i = 0
                for record in records:
                    date_after = GetPatientRegistryReportService._extract_date_after(record.get('period', 'all'))
                    document_type = record.get('document_type', '')
                    medical_services = record.get('medical_services', '').split(',')
                    filters = {'patient_id': patient_id}
                    if date_after:
                        filters['service_time__gte'] = date_after
                    if document_type:
                        filters['document_type'] = document_type
                    if medical_services and not (len(medical_services) == 1 and medical_services[0] == ''):
                        filters['medical_service_id__in'] = medical_services
                    print(f"    {i}: filter={filters}, ", end='')
                    queryset = SEMD.objects.filter(**filters).order_by('patient_id', '-service_time')
                    print(f"qty={len(queryset)}, ", end='')
                    entries = record.get('entries', 'last').split(',')
                    print(f"entries={entries}, ", end='')
                    r_ids = GetPatientRegistryReportService._get_queryset_ids(queryset, entries)
                    ids = ids.union(r_ids)
                    print(f"r_ids={r_ids}")
                    i += 1
                if grouped:
                    orders = ['patient_id', 'medical_service_id', '-service_time']
                else:
                    orders = ['patient_id', '-service_time']
                queryset = SEMD.objects.\
                    filter(patient_id=patient_id, internal_message_id__in=list(ids)).\
                    order_by(*orders)
                print(f"    len semds = {len(queryset)}")
            else:
                queryset = SEMD.objects.none()
        else:
            queryset = SEMD.objects.none()
        return queryset

    @staticmethod
    def _get_semd_tests(patient_id, registry_report_settings, section, grouped=False):
        print(f'GET Semd Tests, section={section}')
        settings = registry_report_settings.get(section, None)
        if settings:
            records = settings.get('records', None)
            if records:
                ids = set()
                i = 0
                for record in records:
                    date_after = GetPatientRegistryReportService._extract_date_after(record.get('period', 'all'))
                    laboratory_tests = record.get('laboratory_tests', '').split(',')
                    filters = {'patient_id': patient_id}
                    if date_after:
                        filters['test_time__gte'] = date_after
                    if laboratory_tests and not (len(laboratory_tests) == 1 and laboratory_tests[0] == ''):
                        filters['laboratory_test_id__in'] = laboratory_tests
                    print(f"    {i}: filter={filters}, ", end='')
                    queryset = SemdTest.objects.filter(**filters).order_by('patient_id', '-test_time')
                    print(f"qty={len(queryset)}, ", end='')
                    entries = record.get('entries', 'last').split(',')
                    print(f"entries={entries}, ", end='')
                    r_ids = GetPatientRegistryReportService._get_queryset_ids(queryset, entries)
                    ids = ids.union(r_ids)
                    print(f"r_ids={r_ids}")
                    i += 1
                if grouped:
                    orders = ['patient_id', 'laboratory_test_id', '-test_time']
                else:
                    orders = ['patient_id', '-test_time']
                queryset = SemdTest.objects.\
                    filter(patient_id=patient_id, id__in=list(ids)).\
                    order_by(*orders)
                print(f"    len semds = {len(queryset)}")
            else:
                queryset = SemdTest.objects.none()
        else:
            queryset = SemdTest.objects.none()
        return queryset

    @staticmethod
    def _extract_date_after(period):
        if period == 'all':
            return None
        months = period.partition('m')[0]
        if not months.isdecimal():
            return None
        months = int(months)
        today = datetime.now().date()
        year, month, day = today.year, today.month, today.day
        year_month_after = year * 12 + month - 1 - months
        year_after = year_month_after // 12
        month_after = year_month_after % 12 + 1
        date_after = datetime(year=year_after, month=month_after, day=day)
        return date_after

    @staticmethod
    def _extract_indexes(entries):
        indexes = list()
        for entry in entries:
            if entry == 'last':
                idx = 0
            elif entry == 'first':
                idx = -1
            elif entry.isdecimal():
                idx = int(entry)
            elif entry.partition('last-')[2].isdecimal():
                idx = int(entry.partition('last-')[2])
            elif entry.partition('first+')[2].isdecimal():
                idx = -int(entry.partition('first+')[2]) - 1
            else:
                idx = None
            if idx is not None:
                indexes.append(idx)
        return indexes

    @staticmethod
    def _get_queryset_ids(queryset, entries):
        ids = set()
        indexes = GetPatientRegistryReportService._extract_indexes(entries)
        for idx in indexes:
            try:
                pk = queryset[idx].pk
                ids = ids.union({pk})
            except:
                pass
        return ids
