# Create your views here.

import datetime

from models import Speech, Source, Speaker

from chmura.word.views import word_count

#from django.template import Context, RequestContext, loader, Template

from django.template import Context, loader
from django.shortcuts import get_object_or_404
from django.http import HttpResponse as HTTPResponse
#from django.db.models import Avg, Max, Min, Count
#from django.db.models import Max, Min

def speech(request, object_id):
  '''
  * years - a sequence of year strings/objects
  '''
  speech = get_object_or_404 (Speech, pk=object_id)
 
  years = Speech.objects.all().order_by('date')
  sources = Source.objects.filter(speech__exact=speech).order_by('name')

  result = dict ( speech=speech, years=years, sources=sources if sources else None )
  
  result ['word_count'] = word_count (object_id)[:30]
#  result ['words_max'] = result['word_count'][0][1]
  
  template = loader.get_template("speech.html")    
  context = Context(result)

  return HTTPResponse(template.render(context))
