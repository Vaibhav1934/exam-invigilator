# Generated by Django 4.0.3 on 2022-05-03 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_faculty_inv_or_dc_alter_exam_inv_exam_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam_inv',
            name='ses_a',
            field=models.CharField(default='NIL', max_length=3),
        ),
        migrations.AddField(
            model_name='exam_inv',
            name='ses_m',
            field=models.CharField(default='NIL', max_length=3),
        ),
        migrations.AlterField(
            model_name='exam_inv',
            name='exam_date',
            field=models.DateField(default='2022-05-03'),
        ),
    ]
