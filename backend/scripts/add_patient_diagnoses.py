from django.db import transaction, models

from backend.models.patient_models import Patient, PatientDiagnosis, PatientMedicalCard
from backend.models.ref_inf_models import Diagnosis
from backend.models.semd_models import SEMD


def run():
    patients = Patient.objects.all()

    i = 0
    for patient in patients:
        print(i, patient.snils, end=': ')
        diagnoses = set()
        card_amb = set()
        card_sta = set()
        with transaction.atomic():
            semd = SEMD.objects.filter(patient_id=patient.snils).order_by('patient_id')
            for semd_entry in semd:
                if semd_entry.diagnoses is not None and semd_entry.diagnoses != '':
                    row_diagnoses = {d.strip() for d in semd_entry.diagnoses.split(';')}
                    diagnoses = diagnoses.union(row_diagnoses)
                if semd_entry.diagnosis is not None and semd_entry.diagnosis != '':
                    diagnoses = diagnoses.union({semd_entry.diagnosis})
                if semd_entry.med_card_amb is not None and semd_entry.med_card_amb != '':
                    card_amb = card_amb.union({semd_entry.med_card_amb.strip()})
                if semd_entry.med_card_sta is not None and semd_entry.med_card_sta != '':
                    card_sta = card_sta.union({semd_entry.med_card_sta.strip()})
            j, k, l = 0, 0, 0
            for d in diagnoses:
                try:
                    diagnosis = Diagnosis.objects.get(mkb_code=d)
                except Diagnosis.DoesNotExist:
                    diagnosis = None
                if diagnosis is not None:
                    pd = PatientDiagnosis()
                    pd.patient = patient
                    pd.diagnosis = diagnosis
                    pd.save()
                j += 1
            for a in card_amb:
                pc = PatientMedicalCard()
                pc.patient = patient
                pc.card_type = 'amb'
                pc.card_number = a
                pc.save()
                k += 1
            for s in card_sta:
                pc = PatientMedicalCard()
                pc.patient = patient
                pc.card_type = 'sta'
                pc.card_number = s
                pc.save()
                l += 1
            print(diagnoses, len(diagnoses), j, card_amb, len(card_amb), k, card_sta, len(card_sta), l)
        i += 1


