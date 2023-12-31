# Generated by Django 4.2.3 on 2023-07-28 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0023_patientmedicalcard_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='patientmedicalcard',
            name='pat_car__snils_t_n__unq',
        ),
        migrations.RemoveField(
            model_name='patientmedicalcard',
            name='patient_snils',
        ),
        migrations.AddConstraint(
            model_name='patientmedicalcard',
            constraint=models.UniqueConstraint(fields=('patient_id', 'card_type', 'card_number'), name='pat_car__snils_t_n__unq'),
        ),
    ]
