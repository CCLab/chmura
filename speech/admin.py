#

from django.contrib import admin
from models import Speaker, Context, Speech, Source

admin.site.register(Speaker)
admin.site.register(Context)
admin.site.register(Speech)
admin.site.register(Source)

