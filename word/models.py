from django.db import models

# Create your models here.

class Ignore (models.Model):
  word = models.TextField (null=False)
 
class Word (models.Model):
  word = models.TextField (null=False)

class Synonym (models.Model):
  origin = models.ForeignKey(Word)
  word = models.TextField (null=False)  