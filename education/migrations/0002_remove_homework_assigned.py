# Generated by Django 3.2.9 on 2022-05-18 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homework',
            name='assigned',
        ),
    ]