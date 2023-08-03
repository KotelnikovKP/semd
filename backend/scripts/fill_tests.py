import math

from django.core.management import CommandError
from django.db import transaction

from backend.models.ref_inf_models import LaboratoryTest, MedicalService
from backend.models.semd_models import SEMD, SemdTest

PORTION_ITEMS = 1000


def run():
    semd_count = SEMD.objects.filter(document_type='3').count()
    portions_count = math.ceil(semd_count / PORTION_ITEMS)
    print(semd_count, portions_count)
    fill = not_fill = tests = mss = 0
    for portion in range(portions_count):
        offset = portion * PORTION_ITEMS
        limit = offset + PORTION_ITEMS
        with transaction.atomic():
            semd = SEMD.objects.filter(document_type='3').order_by('internal_message_id')[offset:limit]
            for semd_entry in semd:
                test_codes = [d.strip() for d in semd_entry.test_code.split(';')]
                test_values = [d.strip() for d in semd_entry.test_value.split(';')]
                test_units = [d.strip() for d in semd_entry.test_unit.split(';')]
                mkb10 = set()
                if len(test_codes) == len(test_values) and len(test_codes) == len(test_units):
                    for i, code in enumerate(test_codes):
                        if code != '' and code.isdigit():
                            try:
                                laboratory_test = LaboratoryTest.objects.get(id=int(code))
                                if laboratory_test.mkb10_codes is not None:
                                    laboratory_test_mkb10 = [d.strip() for d in laboratory_test.mkb10_codes.split(';')]
                                    mkb10 = mkb10.union(laboratory_test_mkb10)
                            except LaboratoryTest.DoesNotExist:
                                laboratory_test = None
                                print(semd_entry.internal_message_id, code)
                            if laboratory_test is not None:
                                semd_test = SemdTest()
                                semd_test.semd = semd_entry
                                semd_test.laboratory_test = laboratory_test
                                if test_values[i] == test_units[i]:
                                    semd_test.value = test_values[i]
                                else:
                                    semd_test.value = test_values[i] + ' ' + test_units[i]
                                semd_test.save()
                                tests += 1
                    if semd_entry.medical_service_id is None:
                        if len(mkb10) == 1:
                            try:
                                medical_service = MedicalService.objects.get(ms_code=list(mkb10)[0])
                            except MedicalService.DoesNotExist:
                                medical_service = None
                            if medical_service is not None:
                                semd_entry.medical_service = medical_service
                                semd_entry.save()
                                mss += 1
                    fill += 1
                else:
                    not_fill += 1
        print(f'{portion}: fill={fill}, tests={tests}, ms={mss}, not_fill={not_fill}')
