# Generated by Django 3.2.9 on 2021-12-22 11:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0005_alter_homework_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 23, 11, 49, 4, 664125, tzinfo=utc), verbose_name='Дата дедлайна'),
        ),
    ]
