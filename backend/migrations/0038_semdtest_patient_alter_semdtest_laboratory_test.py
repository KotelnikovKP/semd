# Generated by Django 4.2.3 on 2023-08-03 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0037_remove_semd_end_date_str_remove_semd_start_date_str_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='semdtest',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tests', to='backend.patient', verbose_name='Patient'),
        ),
        migrations.AlterField(
            model_name='semdtest',
            name='laboratory_test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tests', to='backend.laboratorytest', verbose_name='Laboratory test'),
        ),
    ]
