# Create your views here.

import datetime

from models import Speech, Source, Speaker

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
  template = loader.get_template("speech.html")    
  context = Context(result)

  return HTTPResponse(template.render(context))
