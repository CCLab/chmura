from django.db import models

from chmura.speech.models import Speech

import sys

# Create your models here.

class Lemma (models.Model):
  'The basic form of a word.'
  word = models.TextField (null=False, unique=True)
  
  def __unicode__(self):
    return self.word
#    return unicode(self.word.decode('utf-8')).encode(sys.stdout.encoding)

class Ignore (models.Model):
  'Words to be ignored.'
  lemma = models.ForeignKey(Lemma, unique=True)
   
class Dict (models.Model):
  lemma = models.ForeignKey (Lemma)
  word = models.TextField (null=False, unique=True)
   
class Word (models.Model):
  '''
  * lemma - lemma of the word, for example "sejm"
  * word  - "clean" form of the word, for example "sejmie"
  * display - actual form of the word in the text, with case and following diacritics,
    for example "Sejmie!"

  do wywalenia?
  '''
  
  lemma = models.ForeignKey (Lemma, related_name='lemma_set', null=False)
  prev = models.ForeignKey ('self', related_name='prev_set', null=True)  
  next = models.ForeignKey ('self', related_name='next_set', null=True)
  speech = models.ForeignKey (Speech)
  word = models.TextField (blank=False)
  display = models.TextField (null=False)  
   
  
#class Words (models.Model):
#
#  speech = models.ForeignKey(Speech, null=False)
#  lemma = models.ForeignKey(Lemma, null=False)
#  order = models.IntegerField()
#  word = models.TextField(null=False)
  
class Compound (models.Model):

  lemma = models.ForeignKey(Lemma)
  first = models.BooleanField(default=False, blank=False)
  next = models.ForeignKey('Compound', blank=True, null=True)
  
  def __unicode__ (self):
  
    return self.lemma.word
  
  