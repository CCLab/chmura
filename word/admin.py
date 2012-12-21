#

from django.contrib import admin
from models import Lemma, Dict, Word

admin.site.register(Lemma)
admin.site.register(Word)
admin.site.register(Dict)
#admin.site.register(Source)
