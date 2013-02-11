# Create your views here. 

import sys, json

from operator import itemgetter

from django.http import HttpResponse as HTTPResponse
from django.template import Context, RequestContext, loader, Template
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
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

### NOT A VIEW EITHER


def normalize_stat_queryset (qs):

   max = float(qs.aggregate(Max('count'))['count__max'])
   return  [ (s.lemma.word, str((float(s.count)/max)*3).replace(',','.'), s.count, s.lemma.id) for s in qs ]
  


### views

def api_count (request, speech_id):
  'returns lemma count dictionary of the specified speech, recounted'  
  return HTTPResponse (Context(unicode(json.dumps(word_count(speech_id)[:20],
                       ensure_ascii=False))))              
                       
def word (request, object_id):
  '''
  WARNING: the Word model may contain only one copy of each Speech text for this to work!
  '''

  WIDTH = 20
  
  lemma = get_object_or_404(Lemma, pk=object_id)
  stats = Stat.objects.filter(lemma__exact=lemma)
  speeches = Speech.objects.all().order_by('-date')
  sum = 0
  counts = []
  years = []  
  
  for speech in speeches:
    count = Word.objects.filter(lemma__exact=lemma, speech__exact=speech).count()    
    counts.append ((speech, count))
#    years.append(speech)
    sum = sum+count
    
  m = max([ int(item[1]) for item in counts ] )
  result = [ (item[0], item[1], str((float(item[1])/m)*WIDTH)) for item in counts ]
  
  template = loader.get_template("word.html")
  
  return HTTPResponse(template.render(Context({'counts':result,'yearsactive':'active',
    'speechactive':'off', 'sum': sum, 'word': lemma.word, 'years': years })))
  

def year (request, object_id, width=4):

  NUMWORDS=20

  'year comparison views'

  speech = get_object_or_404 (Speech, pk=object_id)
  speeches = Speech.objects.filter(date__gte=speech.date)[:int(width)]
  stats = Stat.objects.filter(speech__in=speeches)
  prev_speech = Speech.objects.filter(date__lte=speech.date).order_by('date')[0]
  next_speech = Speech.objects.filter(date__gte=speeches[len(speeches)].date).order_by('-date')[0]  
  
  array = []
    
  for speech in speeches:
  
    words = stats.filter(speech__exact=speech).order_by('-count')
    array.append( ( speech.date.year, normalize_stat_queryset(words[:NUMWORDS])) )

  result = {'array': array, 'yearsactive': 'active', 'speechactive': 'off', 'prev': prev_speech, 'next': next_speech}
  template = loader.get_template("year.html")
  
  return HTTPResponse(template.render(Context(result)))


def context(request, speech_id, lemma_id):
 
  WIDTH = 4

  lemma = get_object_or_404 (Lemma, pk=lemma_id)
  speech = get_object_or_404 (Speech, pk=speech_id)
  words = Word.objects.filter(speech__exact=speech, lemma__exact=lemma).order_by('id')
  
  result = []
  for w in words:
    context, prev = [], []
    p = w
    for i in xrange(WIDTH):
      p = p.prev
      prev.append((p,None))
      
    prev.reverse()
    context = prev
    context.append((w, True))
    n = w
    for i in xrange(WIDTH):
      n = n.next
      context.append((n, None))

    result.append(tuple(context))

  template = loader.get_template("context.html")
  
  return HTTPResponse(template.render(Context(dict(context=result, 
    count=words.count(), word=lemma, speech=speech))))

###

@login_required
def cache (request):    

  'trigger this view after uploading new speech to update stats cache'
  
  speeches = Speech.objects.all()
  
  for speech in speeches:
    count = word_count(speech.id)
    
    for item in count:
      stat, created = Stat.objects.get_or_create(speech=speech, lemma=item[0], count=item[1])
      
      if created:
        stat.save()

  return HTTPResponse()
