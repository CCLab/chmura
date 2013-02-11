# Create your views here.

import datetime

from models import Speech, Source, Speaker

# from chmura.word.views import word_count

from chmura.word.models import Stat

#from django.template import Context, RequestContext, loader, Template

from django.template import Context, loader
from django.shortcuts import get_object_or_404
from django.http import HttpResponse as HTTPResponse
from django.http import HttpResponseRedirect as HTTPResponseRedirect
#from django.db.models import Avg, Max, Min, Count
from django.db.models import Max, Min

from django.core.urlresolvers import reverse

def speech(request, object_id):
  '''
  * years - a sequence of year strings/objects
  '''
  
  NUMWORDS = 50
  
  speech = get_object_or_404 (Speech, pk=object_id)
 
  years = [ (s, s==speech ) for s in Speech.objects.all().order_by('-date') ]
  sources = Source.objects.filter(speech__exact=speech).order_by('name')

  result = dict ( speech=speech, years=years, speechactive='active', yearsactive='off',
    sources=sources if sources else None )
  
  counted = Stat.objects.filter(speech__exact=speech).order_by('-count')
  if counted:
    words = counted [:NUMWORDS]
    max = float(counted.aggregate(Max('count'))['count__max'])
    f = [ (s.lemma.word, str((float(s.count)/max)*5).replace(',','.'), s.lemma.id) for s in words ]
    result ['word_count'] = f
  else:
    result ['word_count'] = []          

  result['context_script'] = True
  
  template = loader.get_template("speech.html")
  context = Context(result)
                            
  return HTTPResponse(template.render(context))

def main(request):

  'main page view'
  
  speech = Speech.objects.all().order_by('-date')[0]
  
  return HTTPResponseRedirect(reverse('chmura.speech.views.speech', kwargs={'object_id':speech.id}))
  