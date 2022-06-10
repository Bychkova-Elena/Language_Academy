# Generated by Django 3.2.9 on 2022-06-10 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='city_en',
            field=models.CharField(default='', max_length=20, null=True, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='city_ru',
            field=models.CharField(default='', max_length=20, null=True, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='firstName_en',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='firstName_ru',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lastName_en',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='Фамилия'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lastName_ru',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='Фамилия'),
        ),
    ]