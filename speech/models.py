from django.db import models

# Create your models here.

class Speaker (models.Model):
  name = models.TextField()
  function = models.TextField()
  head = models.ImageField()
  
class Context(models.Model):
  date = models.DateField (auto_add_now=False)
  cabinet = models.TextField()
  background = models.textField()
  
class Speech(models.Model):
  order = models.IntegerField()  
  
class Source (models.Model):
  speech = models.ForeignKey(Speech)
  url = models.UrlField()
