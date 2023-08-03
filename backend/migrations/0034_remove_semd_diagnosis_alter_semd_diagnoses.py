# Generated by Django 4.2.3 on 2023-08-02 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0033_remove_semd_doctor_job_title_remove_semd_mo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semd',
            name='diagnosis',
        ),
        migrations.AlterField(
            model_name='semd',
            name='diagnoses',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Diagnosis codes'),
        ),
    ]
