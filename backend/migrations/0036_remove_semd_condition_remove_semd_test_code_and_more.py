# Generated by Django 4.2.3 on 2023-08-03 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0035_semdtest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='semd',
            old_name='condition',
            new_name='place_of_service',
        ),
        migrations.RemoveField(
            model_name='semd',
            name='test_code',
        ),
        migrations.RemoveField(
            model_name='semd',
            name='test_unit',
        ),
        migrations.RemoveField(
            model_name='semd',
            name='test_value',
        ),
    ]
