# Generated by Django 4.2.3 on 2023-07-27 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_diagnosis'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalOrganization',
            fields=[
                ('oid', models.CharField(max_length=35, primary_key=True, serialize=False, verbose_name='Medical organization code')),
                ('id', models.IntegerField(verbose_name='Identifier')),
                ('nameFull', models.CharField(max_length=400, verbose_name='Medical organization full name')),
                ('nameShort', models.CharField(blank=True, max_length=350, null=True, verbose_name='Medical organization short name')),
                ('medicalSubjectId', models.IntegerField(blank=True, null=True, verbose_name='Medical subject code')),
                ('medicalSubjectName', models.CharField(blank=True, max_length=140, null=True, verbose_name='Medical subject name')),
                ('inn', models.CharField(blank=True, max_length=12, null=True, verbose_name='INN')),
                ('kpp', models.CharField(blank=True, max_length=9, null=True, verbose_name='KPP')),
                ('ogrn', models.CharField(blank=True, max_length=15, null=True, verbose_name='OGRN')),
                ('regionId', models.IntegerField(blank=True, null=True, verbose_name='Region code')),
                ('regionName', models.CharField(blank=True, max_length=50, null=True, verbose_name='Region name')),
                ('moAgencyKind', models.CharField(blank=True, max_length=70, null=True, verbose_name='Agency kind')),
            ],
            options={
                'verbose_name': 'Medical organization',
                'verbose_name_plural': 'Medical organizations',
                'ordering': ['oid'],
            },
        ),
        migrations.AddIndex(
            model_name='diagnosis',
            index=models.Index(fields=['name'], name='dia__name__idx'),
        ),
        migrations.AddIndex(
            model_name='medicalorganization',
            index=models.Index(fields=['nameShort'], name='med_org__name__idx'),
        ),
        migrations.AddIndex(
            model_name='medicalorganization',
            index=models.Index(fields=['id'], name='med_org__id__idx'),
        ),
    ]
