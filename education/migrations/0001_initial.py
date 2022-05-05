
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0020_alter_userprofile_role'),
        ('languages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Курс')),
                ('price', models.PositiveIntegerField(default=0, help_text='указывать цену в рублях', verbose_name='Цена')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='languages.language', verbose_name='Язык')),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='languages.level', verbose_name='Уровень')),
                ('student', models.ManyToManyField(to='auth.Student', verbose_name='Студент')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.teacher', verbose_name='Учитель')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starts', models.CharField(max_length=350, verbose_name='Дата и время первого занятия')),
                ('end', models.CharField(max_length=350, verbose_name='Дата окончания занятия')),
                ('period', models.CharField(max_length=350, verbose_name='Промежуток между занятиями периода')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Расписание',
                'verbose_name_plural': 'Расписания',
            },
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Домашнее задание')),
                ('link', models.URLField(blank=True, null=True)),
                ('descrition', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('deadline', models.DateTimeField(verbose_name='Дата дедлайна')),
                ('onEveryLesson', models.BooleanField(default=False, verbose_name='Длительное')),
                ('draft', models.BooleanField(default=False, verbose_name='Черновик')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='education.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Домашнее задание',
                'verbose_name_plural': 'Домашние задания',
            },
        ),
    ]
