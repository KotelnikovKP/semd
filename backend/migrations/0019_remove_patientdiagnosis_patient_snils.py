# Generated by Django 4.2.3 on 2023-07-28 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_alter_patientdiagnosis_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientdiagnosis',
            name='patient_snils',
        ),
    ]
