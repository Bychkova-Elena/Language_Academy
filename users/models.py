from django.db import models
from django.contrib.auth.models import User
from languages.models import Language

from rest_framework_simplejwt.tokens import RefreshToken 

class UserProfile(models.Model):
    
    STUDENT = 'STUDENT'
    TEACHER = 'TEACHER'
    ROLE = [
        (STUDENT, 'STUDENT'),
        (TEACHER, 'TEACHER')
    ]
    
    user = models.OneToOneField(User,verbose_name="Пользователь", on_delete=models.CASCADE)
    role = models.CharField("Роль",
                              max_length=20,
                              choices=ROLE,
                              default=STUDENT)
    firstName = models.CharField(verbose_name="Имя", max_length=255, default='')
    lastName = models.CharField(verbose_name="Фамилия", max_length=255, default='')
    phone = models.CharField(verbose_name="Телефон", max_length=20, default='')
    city = models.CharField(verbose_name="Город", max_length=20, default='')

    def __str__(self):
        return self.firstName
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access': str(refresh.access_token)
        }
        
    class Meta:
        app_label = 'auth'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профиль пользователей'
        ordering = ('user',)

    
class Teacher(models.Model):
    '''Учителя'''
    
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
    '''Ученики'''

    user = models.OneToOneField(User,verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    class Meta:
        app_label = 'auth'
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        ordering = ('user',)
