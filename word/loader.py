#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, fileinput, string, codecs

from chmura.word.models import Lemma, Dict, Ignore, Word

STRIP = u'.,;?!:-@#$%^&*()+_'

LETTERS = tuple(string.ascii_letters) + ('ą','ć','ę','ł','ń','ó','ś','ż','ź')

from django.db import IntegrityError

import django.db

def clean_word(word):
  'returns only polish letters of the word'

  return word.lower().strip().strip(STRIP)

# print w
#  if w:
#    result = []
#    for l in w:
#      print ord(l)
#      if l in LETTERS:
#        result.append(l)

#  print result        
#  if result:
#    return ''.join(result)

def dict_lookup(word):
  'looking for word in the known dictionary'

  try:
    dict = Dict.objects.get(word=word)
    return dict.lemma
  except Dict.DoesNotExist:
    return None
        
def dict_add(word):

  def input_lemma(word):
  
    'manual input of the lemma'
    
#    l = raw_input('Enter lemma: ').decode(sys.stdin.encoding)
    l = raw_input('Enter lemma: ').decode('utf-8')    
    lemma = Lemma(word=l)
#    print lemma
    try: 
      lemma.save()
    except IntegrityError:
      lemmas = Lemma.objects.filter(word__exact=word)
      if lemmas:
        lemma = lemmas[0]
      else:
        lemma = None

    return lemma
 
  if not dict_lookup(word):
  
    lemmas =  Lemma.objects.filter(word__contains=word[:5])
    lemma = None
  
    if len(lemmas) == 0:
      lemma = input_lemma(word)
  
    elif len(lemmas) == 1:
        lemma = lemmas[0]
        print lemma.id
        try: 
          resp = raw_input (u'lemma [%s] ok? '.decode('utf-8') % unicode(lemma.word))
        except UnicodeError:
          resp = 'y'
        if resp == 'y':
          pass
#          try:
#            dict_entry = Dict(word=word, lemma=lemma)
#            dict_entry.save()
#          except django.db.IntegrityError:
#            pass # already in the dictionary
        else:
          lemma = input_lemma(word)
      
    elif len(lemmas) > 1:
      while not lemma:  
        for l, num in zip (lemmas, xrange(len(lemmas)+1)):
          print '[%d] %s' % (num, l), 
      
        print ''
        resp = raw_input ('enter lemma number or i for manual input: ')
    
        if resp == 'i':
          lemma = input_lemma(word)
            
          print 'l', lemma
        else:
          try:
            lemma = lemmas[int(resp)]
          except ValueError:
            continue
    try:    
      dict_entry = Dict(word=word, lemma=lemma)
      dict_entry.save()      
    except IntegrityError:
      pass # to be debugged



    return dict_entry

if __name__ == "__main__":
  if len(sys.argv) > 1:
  
    last_word = None
    for line in fileinput.input(sys.argv[1:], 
                                openhook=lambda f,m:codecs.open(f,m, encoding='utf-8')):
  
      words = line.split()
    
      if words:

        for text_word in words:
        
#          clean_word = unicode(text_word.strip(STRIP).lower().decode('utf-8'))
          clean = clean_word(text_word)
          
          print clean

          lemma = dict_lookup(clean)

          if not lemma:
          
            dict_entry = dict_add(clean)

            lemma = dict_entry.lemma          
                 
            word = Word(display=text_word, word=clean, prev=last_word, next=None, lemma=lemma)

            try:             
              word.save()
#            except django.db.IntegrityError:
#              pass #should not happen
            
              if last_word:
                last_word.next = word
                last_word.save()
            
              last_word=word
        
            except django.db.IntegrityError:
              print 'WE ARE ALL GONNA DIE!!!'
              pass #should not happen
