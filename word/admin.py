#

from django.contrib import admin
from models import Lemma, Dict, Word, Ignore, Compound

admin.site.register(Lemma)
admin.site.register(Word)
admin.site.register(Dict)
admin.site.register(Ignore)
admin.site.register(Compound)
