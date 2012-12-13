from django.db import models

# Create your models here.

class Cabinet (models.Model):
  name = models.TextField()
  
  def __str__(self):
    return self.name

class Speaker (models.Model):
  name = models.TextField()
  function = models.TextField()
  head = models.ImageField(upload_to='uploads')
  
  def __str__(self):
    return "%s: %s" % (self.name, self.function)
    
class Speech(models.Model):
  speaker = models.ForeignKey(Speaker)
  date = models.DateField ()  
  background = models.TextField ()
  cabinet = models.ForeignKey (Cabinet)
  
  def __str__(self):
    return "%s: %s" % (self.date, self.background)
  
class Source (models.Model):
  speech = models.ForeignKey (Speech)
  url = models.URLField (max_length=1024)
  name = models.TextField ()

  def __str__(self):
    return "%s: %s" % (self.url, self.name)