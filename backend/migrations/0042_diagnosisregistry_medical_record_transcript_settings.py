# Generated by Django 4.2.3 on 2023-08-05 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0041_semdtest_semd_test__time__idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnosisregistry',
            name='medical_record_transcript_settings',
            field=models.JSONField(default={}, verbose_name='Settings of medical record transcript'),
            preserve_default=False,
        ),
    ]
