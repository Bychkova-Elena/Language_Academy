# Generated by Django 3.2.9 on 2022-01-30 15:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0008_alter_homework_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 31, 15, 12, 31, 717249, tzinfo=utc), verbose_name='Дата дедлайна'),
        ),
    ]
