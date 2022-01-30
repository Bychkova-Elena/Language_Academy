from django.db import models
from django.contrib.auth.models import User
from languages.models import Language

class UserProfile(models.Model):
    
    STUDENT = 'STUDENT'
    TEACHER = 'TEACHER'
    ROLE = [
        (STUDENT, 'STUDENT'),
        (TEACHER, 'TEACHER')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField("Роль",
                              max_length=20,
                              choices=ROLE,
                              default=STUDENT)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=20, default='')
    city = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.first_name
        
    class Meta:
        app_label = 'auth'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профиль пользователей'
    
class Teacher(models.Model):
    '''Учителя'''

    user = models.OneToOneField(
        UserProfile, verbose_name="Пользователь", on_delete=models.CASCADE)
    language = models.ManyToManyField(Language, verbose_name="Язык")

    def __str__(self):
        return str(self.user)

    class Meta:
        app_label = 'auth'
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


class Student(models.Model):
    '''Ученики'''

    user = models.OneToOneField(
        UserProfile, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    class Meta:
        app_label = 'auth'
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
