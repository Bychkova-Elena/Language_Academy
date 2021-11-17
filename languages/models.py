from django.db import models

class Language(models.Model):
  '''Языки'''
  name = models.CharField("Язык", max_length = 150)
  
  def __str__(self):
    return self.name

  class Meta:
    verbose_name = 'Язык'
    verbose_name_plural = 'Языки'
    
    
class Level(models.Model):
  '''Уровни'''
  name = models.CharField("Уровень", max_length = 50)
  
  def __str__(self):
    return self.name

  class Meta:
    verbose_name = 'Уровень'
    verbose_name_plural = 'Уровни'
