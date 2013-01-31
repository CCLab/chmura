# Create your views here.

import datetime

from models import Speech, Source, Speaker

# from chmura.word.views import word_count

from chmura.word.models import Stat

#from django.template import Context, RequestContext, loader, Template

from django.template import Context, loader
from django.shortcuts import get_object_or_404
from django.http import HttpResponse as HTTPResponse
#from django.db.models import Avg, Max, Min, Count
from django.db.models import Max, Min

def speech(request, object_id):
  '''
  * years - a sequence of year strings/objects
  '''
  
  NUMWORDS = 50
  
  speech = get_object_or_404 (Speech, pk=object_id)
 
  years = Speech.objects.all().order_by('-date')
  sources = Source.objects.filter(speech__exact=speech).order_by('name')

  result = dict ( speech=speech, years=years, sources=sources if sources else None )
  
  counted = Stat.objects.filter(speech__exact=speech).order_by('-count')
  if counted:
    words = counted [:NUMWORDS]
    max = float(counted.aggregate(Max('count'))['count__max'])
    print max

    f = [ (s.lemma.word, str((float(s.count)/max)*5).replace(',','.')) for s in words ]
    print f
    result ['word_count'] = f
  else:
    result ['word_count'] = []          

  template = loader.get_template("speech.html")
  context = Context(result)
                            
  return HTTPResponse(template.render(context))
