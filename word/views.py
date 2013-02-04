# Create your views here. 

import sys, json
from operator import itemgetter

from django.http import HttpResponse as HTTPResponse
from django.template import Context, RequestContext, loader, Template
from django.shortcuts import get_object_or_404
from django.db.models import Max
from models import Word, Lemma, Ignore, Compound, Stat
from chmura.speech.models import Speech

### utility function
# THIS IS NOT A VIEW

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

  return result

def normalize_stat_queryset (qs):

   max = float(qs.aggregate(Max('count'))['count__max'])
   return  [ (s.lemma.word, str((float(s.count)/max)*5).replace(',','.'), s.count) for s in qs ]
  
### views

def api_count (request, speech_id):
  'returns lemma count dictionary of the specified speech, recounted'  
  return HTTPResponse (Context(unicode(json.dumps(word_count(speech_id)[:20],
                       ensure_ascii=False))))              
                       
def word (request, object_id):
  '''
  WARNING: the Word model may contain only one copy of each Speech text for this to work!
  '''

  lemma = get_object_or_404(Lemma, pk=object_id)
  stats = Stat.objects.filter(lemma__exact=lemma)
  speeches = Speech.objects.all().order_by('-date')

  print stats
  
  result = []
  
  for speech in speeches:
    count = Stat.objects.filter(lemma__exact=lemma, speech__exact=speech).count()    
    result.append ((speech.date.year, count))

  template = loader.get_template("word.html")
  
  return HTTPResponse(template.render(Context(dict(counts = result))))
  

def year (request, object_id, width=3):

  NUMWORDS=20

  'year comparison views'

  speech = get_object_or_404 (Speech, pk=object_id)
  speeches = Speech.objects.filter(date__gte=speech.date)[:int(width)]
  stats = Stat.objects.filter(speech__in=speeches)
  
  array = []
    
  for speech in speeches:
  
    words = stats.filter(speech__exact=speech).order_by('-count')
    array.append( ( speech.date.year, normalize_stat_queryset(words[:NUMWORDS])) )

  result = dict(array=array)
  template = loader.get_template("year.html")
  
  return HTTPResponse(template.render(Context(result)))

def cache (request):    

  'trigger this view after uploading new speech to update stats cache'
  
  speeches = Speech.objects.all()
  
  for speech in speeches:
    count = word_count(speech.id)
    
    for item in count:
      stat, created = Stat.objects.get_or_create(speech=speech, lemma=item[0], count=item[1])
      
      if created:
        stat.save()
        print stat

  return HTTPResponse()
    
    