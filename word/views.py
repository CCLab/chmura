# Create your views here.

import sys, json

from django.http import HttpResponse as HTTPResponse
from django.template import Context, RequestContext, loader, Template
from operator import itemgetter


from models import Word, Lemma


def word_count (speech_id):

  words = Word.objects.filter(speech__exact=speech_id)
  
  lemmas = (set ( [ word.lemma for word in words ] ))
  
  result = []
  
  for lemma in lemmas:
  
    count = Word.objects.filter(lemma__exact=lemma).count()
    
    result.append((unicode(lemma.word), count))
    
 
  result.sort(key=itemgetter(1)) 
  result.reverse()

  return result
  

def api_count (request, speech_id):
  
  return HTTPResponse (Context(unicode(json.dumps(word_count(speech_id)[:20],
                       ensure_ascii=False))))