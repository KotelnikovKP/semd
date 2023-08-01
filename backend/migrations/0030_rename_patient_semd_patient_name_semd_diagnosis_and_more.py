# Generated by Django 4.2.3 on 2023-08-01 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0029_alter_semd_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='semd',
            old_name='patient',
            new_name='patient_name',
        ),
        migrations.AddField(
            model_name='semd',
            name='diagnosis',
            field=models.CharField(blank=True, null=True, verbose_name='Doctor visit diagnosis'),
        ),
        migrations.AddField(
            model_name='semd',
            name='document_type',
            field=models.CharField(default=2, max_length=8, verbose_name='Structured Electronic Medical Document type'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='semd',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Hospital end date'),
        ),
        migrations.AddField(
            model_name='semd',
            name='end_date_str',
            field=models.CharField(blank=True, null=True, verbose_name='Hospital end date str'),
        ),
        migrations.AddField(
            model_name='semd',
            name='hospitalization_results',
            field=models.CharField(blank=True, null=True, verbose_name='Hospital results'),
        ),
        migrations.AddField(
            model_name='semd',
            name='hospitalization_urgency',
            field=models.CharField(blank=True, null=True, verbose_name='Hospital urgency'),
        ),
        migrations.AddField(
            model_name='semd',
            name='medical_position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='semd', to='backend.medicalposition', verbose_name='Medical position'),
        ),
        migrations.AddField(
            model_name='semd',
            name='mo',
            field=models.CharField(blank=True, max_length=35, null=True, verbose_name='Medical organization code'),
        ),
        migrations.AddField(
            model_name='semd',
            name='patient_condition',
            field=models.CharField(blank=True, null=True, verbose_name='Doctor visit patient condition'),
        ),
        migrations.AddField(
            model_name='semd',
            name='patient_in_condition',
            field=models.CharField(blank=True, null=True, verbose_name='Hospital patient in condition'),
        ),
        migrations.AddField(
            model_name='semd',
            name='patient_out_condition',
            field=models.CharField(blank=True, null=True, verbose_name='Hospital patient out condition'),
        ),
        migrations.AddField(
            model_name='semd',
            name='service',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Medical service code'),
        ),
        migrations.AddField(
            model_name='semd',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Hospital start date'),
        ),
        migrations.AddField(
            model_name='semd',
            name='start_date_str',
            field=models.CharField(blank=True, null=True, verbose_name='Hospital start date str'),
        ),
        migrations.AddField(
            model_name='semd',
            name='test_code',
            field=models.CharField(blank=True, null=True, verbose_name='Tests codes'),
        ),
        migrations.AddField(
            model_name='semd',
            name='test_unit',
            field=models.CharField(blank=True, null=True, verbose_name='Tests units'),
        ),
        migrations.AddField(
            model_name='semd',
            name='test_value',
            field=models.CharField(blank=True, null=True, verbose_name='Tests values'),
        ),
    ]
