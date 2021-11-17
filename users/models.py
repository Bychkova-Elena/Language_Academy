from django.db import models
from django.contrib.auth.models import User
from languages.models import Language


class Teacher(models.Model):
    '''Учителя'''

    user = models.OneToOneField(
        User, verbose_name="Пользователь", on_delete=models.CASCADE)
    language = models.ManyToManyField(Language, verbose_name="Язык")

    def __str__(self):
        return self.user

    class Meta:
        app_label = 'auth'
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


class Student(models.Model):
    '''Ученики'''

    user = models.OneToOneField(
        User, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return self.user

    class Meta:
        app_label = 'auth'
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
