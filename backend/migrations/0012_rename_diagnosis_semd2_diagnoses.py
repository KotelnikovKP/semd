# Generated by Django 4.2.3 on 2023-07-27 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_remove_semd2_mo_remove_semd2_service_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='semd2',
            old_name='diagnosis',
            new_name='diagnoses',
        ),
    ]
