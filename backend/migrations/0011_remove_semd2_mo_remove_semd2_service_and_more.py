# Generated by Django 4.2.3 on 2023-07-27 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_remove_semd2_diagnosis_1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semd2',
            name='mo',
        ),
        migrations.RemoveField(
            model_name='semd2',
            name='service',
        ),
        migrations.AddField(
            model_name='semd2',
            name='service_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Medical service date time'),
        ),
    ]
