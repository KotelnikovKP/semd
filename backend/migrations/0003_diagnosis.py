# Generated by Django 4.2.3 on 2023-07-27 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_alter_medicalservice_dateout'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('mkb_code', models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='Diagnosis code (MKB-10)')),
                ('rec_code', models.CharField(max_length=15, verbose_name='Sorted code')),
                ('id', models.IntegerField(verbose_name='Identifier')),
                ('id_parent', models.IntegerField(blank=True, null=True, verbose_name='Parent identifier')),
                ('name', models.CharField(max_length=300, verbose_name='Diagnosis name')),
                ('add_code', models.IntegerField(blank=True, null=True, verbose_name='Addition code')),
                ('rel', models.IntegerField(verbose_name='Sign of relevance')),
                ('dateout', models.DateField(blank=True, null=True, verbose_name='Date out')),
            ],
            options={
                'verbose_name': 'Diagnosis',
                'verbose_name_plural': 'Diagnoses',
                'ordering': ['rec_code'],
                'indexes': [models.Index(fields=['rec_code'], name='dia__rec_code__idx'), models.Index(fields=['id'], name='dia__id__idx'), models.Index(fields=['id_parent'], name='dia__id_parent__idx')],
            },
        ),
    ]
