# Generated by Django 4.2.3 on 2023-07-28 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_remove_patientdiagnosis_patient_snils'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientdiagnosis',
            name='diagnosis_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='patients', to='backend.diagnosis', verbose_name='diagnosis'),
        ),
    ]
