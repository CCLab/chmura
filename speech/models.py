from django.db import models

# Create your models here.

class Speaker (models.Model):
  name = models.TextField()
  function = models.TextField()
  head = models.ImageField(upload_to='uploads')
  
class Context(models.Model):
  cabinet = models.TextField()
  
class Speech(models.Model):
  date = models.DateField ()  
  background = models.TextField ()
  
class Source (models.Model):
  speech = models.ForeignKey (Speech)
  url = models.URLField (max_length=1024, )
