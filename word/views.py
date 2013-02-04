# Create your views here. 

import sys, json
from operator import itemgetter

from django.http import HttpResponse as HTTPResponse
from django.template import Context, RequestContext, loader, Template
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from models import Word, Lemma, Ignore, Compound, Stat
from chmura.speech.models import Speech

### utility function

def word_count (speech_id):

  compound_starts = Compound.objects.filter(first__exact=True)
  compound_lemmas = Lemma.objects.filter(id__in=compound_starts.values_list('lemma', flat=True))

  words = Word.objects.exclude(lemma__id__in=Ignore.objects.all().values_list('lemma',flat=True)).filter(speech__exact=speech_id)
  
  lemmas = (set ( [ word.lemma for word in words ] ))
  
  result = []
  
  for lemma in lemmas:
  
    count = words.filter(lemma__exact=lemma).count()
    
    result.append((lemma, count))
    
  result.sort(key=itemgetter(1)) 
  result.reverse()

#  print result

  return result
  
### views

def api_count (request, speech_id):
  
  return HTTPResponse (Context(unicode(json.dumps(word_count(speech_id)[:20],
                       ensure_ascii=False))))              
                       
def word (request, object_id):
  '''
  WARNING: the Word model may contain only one copy of each Speech text for this to work!
  '''

  lemma = get_object_or_404(Lemma, pk=object_id)
  
  words = Word.objects.filter(lemma__exact=lemma)
  
#  dates = Speech.objects.filter(id__in=words.values_list('speech',flat=True)).values_list('date',flat=True).order_by('date')
  speeches = Speech.objects.filter(id__in=words.values_list('speech',flat=True)).order_by('date')
  
  result = []
  for speech in speeches:
    count = words.filter(speech__exact=speech).count()
    
    result.append((speech, count))
   
  template = loader.get_template("word.html")
  
  return HTTPResponse(template.render(Context(dict(speech_list=result,
                      word=lemma.word, sum=words.count()))))
  

def year (request, object_id, width=3):

  speech = get_object_or_404 (Speech, pk=object_id)
  
  speeches = Speech.objects.filter(date__gte=speech.date)[:int(width)]
  
  result = [ (s.date.year, word_count(s.id)) for s in speeches ]
  
  template = loader.get_template("year.html")
  
  return HTTPResponse(template.render(Context(dict(speeches=result, width=width))))


@login_required
def cache (request):    

  speeches = Speech.objects.all()
  
  for speech in speeches:

#    lemmas =  Lemma.objects.filter(id__in=[ w[0] for w in Word.objects.filter(speech=speech).values_list('lemma')])
    
 #   for lemma in lemmas:
  #    count = Word.objects.filter(lemma__exact=lemma, speech_exact=speech).
    
    count = word_count(speech.id)
    
    for item in count:
    
      stat, created = Stat.objects.get_or_create(speech=speech, lemma=item[0], count=item[1])
      
      if created:
        stat.save()
        print stat

  return HTTPResponse()
