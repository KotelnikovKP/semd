# Generated by Django 4.2.3 on 2023-07-27 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalservice',
            name='dateout',
            field=models.DateField(blank=True, null=True, verbose_name='Date out'),
        ),
    ]
