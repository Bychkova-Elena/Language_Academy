# Generated by Django 3.2.9 on 2022-06-11 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0003_auto_20220610_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='period',
            field=models.PositiveIntegerField(verbose_name='Промежуток между занятиями периода'),
        ),
    ]