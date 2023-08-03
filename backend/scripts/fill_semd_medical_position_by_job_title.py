import math

from django.db import transaction

from backend.models.ref_inf_models import MedicalPosition
from backend.models.semd_models import SEMD

PORTION_ITEMS = 10000


def run():
    semd_count = SEMD.objects.count()
    portions_count = math.ceil(semd_count / PORTION_ITEMS)
    fill = not_fill = 0
    not_fill_job = set()
    for portion in range(portions_count):
        offset = portion * PORTION_ITEMS
        limit = offset + PORTION_ITEMS
        with transaction.atomic():
            semd = SEMD.objects.all().order_by('internal_message_id')[offset:limit]
            for semd_entry in semd:
                if semd_entry.doctor_job_title == 'лаборант':
                    semd_entry.medical_position_id = 158
                    semd_entry.save()
                    fill += 1
                elif semd_entry.doctor_job_title == 'логопед':
                    semd_entry.medical_position_id = 137
                    semd_entry.save()
                    fill += 1
                elif semd_entry.doctor_job_title == 'ИТ-специалист':
                    semd_entry.medical_position_id = 206
                    semd_entry.save()
                    fill += 1
                elif semd_entry.doctor_job_title == 'иные профессии рабочих':
                    semd_entry.medical_position_id = 333
                    semd_entry.save()
                    fill += 1
                elif semd_entry.doctor_job_title == 'лечебное дело':
                    semd_entry.medical_position_id = 7
                    semd_entry.save()
                    fill += 1
                elif semd_entry.doctor_job_title == 'заведующий структурного подразделения (отдела, отделения, лаборатории, кабинета, отряда и другое) медицинской организации - врач-специалист':
                    semd_entry.medical_position_id = 7
                    semd_entry.save()
                    fill += 1
                else:
                    try:
                        medical_position = MedicalPosition.objects.get(name=semd_entry.doctor_job_title)
                    except MedicalPosition.DoesNotExist:
                        medical_position = None
                    except MedicalPosition.MultipleObjectsReturned:
                        print(semd_entry.internal_message_id, semd_entry.doctor_job_title)
                    if medical_position is not None:
                        semd_entry.medical_position = medical_position
                        semd_entry.save()
                        fill += 1
                    else:
                        not_fill_job = not_fill_job.union({semd_entry.doctor_job_title})
                        not_fill += 1
        print(f'{portion}: fill={fill}, not_fill={not_fill}: {not_fill_job}')
