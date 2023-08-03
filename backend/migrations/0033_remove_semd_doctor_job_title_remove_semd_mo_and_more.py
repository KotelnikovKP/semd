# Generated by Django 4.2.3 on 2023-08-02 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0032_remove_semd_med_card_amb_remove_semd_med_card_sta_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semd',
            name='doctor_job_title',
        ),
        migrations.RemoveField(
            model_name='semd',
            name='mo',
        ),
        migrations.RemoveField(
            model_name='semd',
            name='service',
        ),
        migrations.RemoveField(
            model_name='semd',
            name='service_time_str',
        ),
        migrations.AddField(
            model_name='semd',
            name='patient_diagnosis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='semd', to='backend.diagnosis', verbose_name='Doctor visit diagnosis'),
        ),
    ]