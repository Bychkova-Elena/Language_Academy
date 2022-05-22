import django.utils.timezone
from django.db import models
from languages.models import Language, Level
from users.models import Student, Teacher


class Course(models.Model):
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    name = models.CharField(verbose_name="Курс", max_length=150)
    level = models.ForeignKey(
        verbose_name="Уровень",
        to=Level,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    price = models.PositiveIntegerField(
        verbose_name="Цена",
        default=0,
        help_text="указывать цену в рублях",
        null=True,
        blank=True
    )
    language = models.ForeignKey(
        verbose_name="Язык",
        to=Language,
        on_delete=models.PROTECT
    )
    teacher = models.ForeignKey(
        verbose_name="Учитель",
        to=Teacher,
        on_delete=models.PROTECT
    )
    students = models.ManyToManyField(
        verbose_name="Студенты",
        to=Student,
        blank=True
    )

    def __str__(self):
        return str(self.name)


class Homework(models.Model):
    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'

    name = models.CharField(verbose_name="Название", max_length=150)
    link = models.URLField(null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    created = models.DateTimeField(verbose_name="Дата создания", default=django.utils.timezone.now)
    deadline = models.DateTimeField(verbose_name="Дата дедлайна")
    onEveryLesson = models.BooleanField(verbose_name="Длительное", default=False)
    course = models.ForeignKey(
        verbose_name="Курс",
        to=Course,
        on_delete=models.SET_NULL,
        null=True
    )
    draft = models.BooleanField(verbose_name="Черновик", default=False)

    def __str__(self):
        return str(self.name)

class TimeTable(models.Model):
    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'

    course = models.ForeignKey(verbose_name="Курс", to=Course, on_delete=models.CASCADE)
    starts = models.CharField(verbose_name="Дата и время первого занятия", max_length=350)
    end = models.CharField(verbose_name="Дата окончания занятия", max_length=350)
    period = models.CharField(verbose_name="Промежуток между занятиями периода", max_length=350)

    def __str__(self):
        return str(self.course)
