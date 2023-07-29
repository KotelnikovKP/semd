# Generated by Django 4.2.3 on 2023-07-28 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_patient'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientDiagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_snils', models.CharField(max_length=11, verbose_name='Patient SNILS')),
                ('diagnosis', models.CharField(max_length=15, verbose_name='Diagnosis code')),
            ],
            options={
                'verbose_name': 'Patient diagnosis',
                'verbose_name_plural': 'Patients diagnoses',
                'ordering': ['patient_snils'],
                'indexes': [models.Index(fields=['diagnosis'], name='pat_dia__diagnosis__idx')],
            },
        ),
    ]