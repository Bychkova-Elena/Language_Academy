from django.db import models
from languages.models import Language, Level
from users.models import Teacher, Student
import django.utils.timezone


class Course(models.Model):
    '''Курсы'''
    name = models.CharField("Курс", max_length=150)
    level = models.ForeignKey(
        Level, verbose_name="Уровень", on_delete=models.PROTECT, null=True, blank=True)
    price = models.PositiveIntegerField(
        "Цена", default=0, help_text="указывать цену в рублях")
    language = models.ForeignKey(
        Language, verbose_name="Язык", on_delete=models.PROTECT)
    teacher = models.ForeignKey(
        Teacher, verbose_name="Учитель", on_delete=models.PROTECT)
    student = models.ManyToManyField(Student, verbose_name="Студент")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Homework(models.Model):
    '''Домашние задания'''
    name = models.CharField("Домашнее задание", max_length=150)
    url = models.URLField(null=True, blank=True)
    descrition = models.TextField("Описание", null=True, blank=True)
    created = models.DateTimeField(
        "Дата создания", default=django.utils.timezone.now)
    deadline = models.DateTimeField("Дата дедлайна", default=django.utils.timezone.now(
    ) + django.utils.timezone.timedelta(1))
    durable = models.BooleanField("Длительное", default=False)
    course = models.ForeignKey(
        Course, verbose_name="Курс", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'


class TimeTable(models.Model):
    '''Расписание'''
    course = models.ForeignKey(
        Course, verbose_name="Курс", on_delete=models.CASCADE)
    time = models.DateTimeField(
        "Время занятия", default=django.utils.timezone.now)

    def __str__(self):
        return self.course

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
