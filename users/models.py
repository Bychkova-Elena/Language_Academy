from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from languages.models import Language


class UserProfile(models.Model):
    class Meta:
        app_label = 'auth'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профиль пользователей'
        ordering = ('user', )

    STUDENT = 'STUDENT'
    TEACHER = 'TEACHER'
    ROLE = [
        (STUDENT, 'STUDENT'),
        (TEACHER, 'TEACHER')
    ]

    user = models.OneToOneField(
        verbose_name="Пользователь",
        to=User,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        verbose_name="Роль",
        max_length=20,
        choices=ROLE,
        default=""
    )
    firstName = models.CharField(verbose_name="Имя", max_length=255, default='')
    lastName = models.CharField(verbose_name="Фамилия", max_length=255, default='')
    phone = models.CharField(verbose_name="Телефон", max_length=20, default='')
    city = models.CharField(verbose_name="Город", max_length=20, default='')

    def __str__(self):
        return str(self.firstName)

    @staticmethod
    @receiver(post_save, sender=User)
    def CreateProfile(instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

class Teacher(models.Model):
    user = models.OneToOneField(User,verbose_name="Пользователь", on_delete=models.CASCADE)
    language = models.ManyToManyField(Language, verbose_name="Язык", blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        app_label = 'auth'
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'
        ordering = ('user', 'language__name')


class Student(models.Model):
    class Meta:
        app_label = 'auth'
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        ordering = ('user', )

    user = models.OneToOneField(User,verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
