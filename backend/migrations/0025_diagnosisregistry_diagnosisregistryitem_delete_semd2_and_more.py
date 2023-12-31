# Generated by Django 4.2.3 on 2023-07-29 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0024_remove_patientmedicalcard_pat_car__snils_t_n__unq_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiagnosisRegistry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Diagnosis registry name')),
                ('short_name', models.CharField(max_length=25, verbose_name='Diagnosis registry short name')),
            ],
            options={
                'verbose_name': 'Diagnosis registry',
                'verbose_name_plural': 'Diagnosis registers',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DiagnosisRegistryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registers', to='backend.diagnosis', verbose_name='diagnosis')),
                ('registry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diagnoses', to='backend.diagnosisregistry', verbose_name='registry')),
            ],
            options={
                'verbose_name': 'Diagnosis registry item',
                'verbose_name_plural': 'Diagnosis registry items',
                'ordering': ['pk'],
            },
        ),
        # migrations.DeleteModel(
        #     name='SEMD2',
        # ),
        migrations.AddIndex(
            model_name='diagnosisregistry',
            index=models.Index(fields=['name'], name='dia_reg__name__idx'),
        ),
    ]
