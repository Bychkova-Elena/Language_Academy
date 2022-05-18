from django.contrib.auth.models import User
from django.db import models
from languages.models import Language


class UserRole(models.TextChoices):
    STUDENT = 'STUDENT'
    TEACHER = 'TEACHER'


class UserProfile(models.Model):
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профиль пользователей'
        ordering = ('user', )

    user = models.OneToOneField(
        verbose_name="Пользователь",
        to=User,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        verbose_name="Роль",
        max_length=20,
        choices=UserRole.choices,
        default=""
    )
    avatar = models.ImageField(verbose_name='Аватар', null=True, blank=True)
    firstName = models.CharField(verbose_name="Имя", max_length=255, default='')
    lastName = models.CharField(verbose_name="Фамилия", max_length=255, default='')
    phone = models.CharField(verbose_name="Телефон", max_length=20, default='')
    city = models.CharField(verbose_name="Город", max_length=20, default='')

    def __str__(self):
        return str(self.firstName)


class Teachers(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    language = models.ManyToManyField(Language, verbose_name="Язык", blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'
        ordering = ('user', 'language__name')


class Students(models.Model):
    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        ordering = ('user', )

    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
